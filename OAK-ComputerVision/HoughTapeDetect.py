import numpy as np  # numpy - manipulate the packet data returned by depthai
import cv2  # opencv - display the video stream
import depthai  # depthai - access the camera and its data packets
import math

pipeline = depthai.Pipeline()

cam_rgb = pipeline.create(depthai.node.ColorCamera)
cam_rgb.setPreviewSize(640, 400)

xout_rgb = pipeline.create(depthai.node.XLinkOut)
xout_rgb.setStreamName("rgb")
cam_rgb.preview.link(xout_rgb.input)

# xinSpatialCalcConfig = pipeline.createXLinkIn()
# xinSpatialCalcConfig.setStreamName("spatialCalcConfig")

controlIn = pipeline.create(depthai.node.XLinkIn)
controlIn.setStreamName('control')
controlIn.out.link(cam_rgb.inputControl)

# spatialLocationCalculator = pipeline.createSpatialLocationCalculator()

lowerH = 55
upperH = 115

lowerS = 150
upperS = 255

lowerV = 170
upperV = 255

expTime = 2000
sensIso = 200

centerX = 0
centerY = 0
numLines = 0

focal_length_in_pixels = 640 * 0.5 / math.tan(71.9 * 0.5 * math.pi / 180)
distBetweenCameras = 7.5

def getMonoCamera(pipeline, isLeft):
    # Configure mono camera
    mono = pipeline.createMonoCamera()
    # Set Camera Resolution
    mono.setResolution(depthai.MonoCameraProperties.SensorResolution.THE_400_P)
    # mono.setPreviewSize(400, 400)
    if isLeft:
        # Get left camera
        mono.setBoardSocket(depthai.CameraBoardSocket.LEFT)
    else :
        # Get right camera
        mono.setBoardSocket(depthai.CameraBoardSocket.RIGHT)
    return mono

# def getStereoPair(pipeline, monoLeftCam, monoRightCam):
#     stereo = pipeline.createStereoDepth()
#     # stereo.setLeftRightCheck(True)
#     stereo.setSubpixel(False)

#     monoLeftCam.out.link(stereo.left)
#     monoRightCam.out.link(stereo.right)

#     return stereo

def on_change(value):
    print(value)

def getFrame(queue):
  # Get frame from queue
  frame = queue.get()
  # Convert frame to OpenCV format and return
  return frame.getCvFrame()

# Set up left and right cameras
monoLeft = pipeline.createMonoCamera()
monoRight = pipeline.createMonoCamera()
stereo = pipeline.createStereoDepth()

stereo.setOutputDepth(True)
stereo.setOutputRectified(False)
stereo.setConfidenceThreshold(255)
stereo.setLeftRightCheck(False)
stereo.setSubpixel(True)

monoLeft.setResolution(depthai.MonoCameraProperties.SensorResolution.THE_400_P)
monoLeft.setBoardSocket(depthai.CameraBoardSocket.LEFT)
monoRight.setResolution(depthai.MonoCameraProperties.SensorResolution.THE_400_P)
monoRight.setBoardSocket(depthai.CameraBoardSocket.RIGHT)

monoLeft.out.link(stereo.left)
monoRight.out.link(stereo.right)

spatialLocationCalculator = pipeline.createSpatialLocationCalculator()
xoutSpatialData = pipeline.createXLinkOut()
xinSpatialCalcConfig = pipeline.createXLinkIn()

xoutDepth = pipeline.createXLinkOut()
xoutDepth.setStreamName("depth")

spatialLocationCalculator.passthroughDepth.link(xoutDepth.input)
stereo.depth.link(spatialLocationCalculator.inputDepth)

topLeft = depthai.Point2f(0.45, 0.45)
bottomRight = depthai.Point2f(0.55, 0.55)

spatialLocationCalculator.setWaitForConfigInput(False)
config = depthai.SpatialLocationCalculatorConfigData()
config.depthThresholds.lowerThreshold = 100
config.depthThresholds.upperThreshold = 10000
config.roi = depthai.Rect(topLeft, bottomRight)
spatialLocationCalculator.initialConfig.addROI(config)
spatialLocationCalculator.out.link(xoutSpatialData.input)
xinSpatialCalcConfig.out.link(spatialLocationCalculator.inputConfig)

xoutSpatialData.setStreamName("spatialData")
xinSpatialCalcConfig.setStreamName("spatialCalcConfig")

with depthai.Device(pipeline) as device:
    q_rgb = device.getOutputQueue("rgb")
    frame = None

    depthQueue = device.getOutputQueue("depth", maxSize=1, blocking=False)
    spatialCalcQueue = device.getOutputQueue(name="spatialData", maxSize=1, blocking=False)
    spatialCalcConfigInQueue = device.getInputQueue("spatialCalcConfig")

    cv2.namedWindow('HSV Tuner', cv2.WINDOW_AUTOSIZE)
    
    cv2.createTrackbar('Lower H', "HSV Tuner", 0, 255, on_change)
    cv2.createTrackbar('Higher H', "HSV Tuner", 0, 255, on_change)
    cv2.createTrackbar('Lower S', "HSV Tuner", 0, 255, on_change)
    cv2.createTrackbar('Higher S', "HSV Tuner", 0, 255, on_change)
    cv2.createTrackbar('Lower V', "HSV Tuner", 0, 255, on_change)
    cv2.createTrackbar('Higher V', "HSV Tuner", 0, 255, on_change)

    cv2.setTrackbarPos('Lower H', "HSV Tuner", lowerH)
    cv2.setTrackbarPos('Higher H', "HSV Tuner", upperH)
    cv2.setTrackbarPos('Lower S', "HSV Tuner", lowerS)
    cv2.setTrackbarPos('Higher S', "HSV Tuner", upperS)
    cv2.setTrackbarPos('Lower V', "HSV Tuner", lowerV)
    cv2.setTrackbarPos('Higher V', "HSV Tuner", upperV)

    while True:
        controlQueue = device.getInputQueue('control')
        ctrl = depthai.CameraControl()
        ctrl.setManualExposure(expTime, sensIso)
        controlQueue.send(ctrl)

        inDepth = depthQueue.get() # blocking call, will wait until a new data has arrived
        inDepthAvg = spatialCalcQueue.get() # blocking call, will wait until a new data has arrived
        
        depthFrame = inDepth.getFrame()
        depthFrameColor = cv2.normalize(depthFrame, None, 255, 0, cv2.NORM_MINMAX, cv2.CV_8UC1)
        depthFrameColor = cv2.equalizeHist(depthFrameColor)
        depthFrameColor = cv2.applyColorMap(depthFrameColor, cv2.COLORMAP_JET)

        lowerH = cv2.getTrackbarPos('Lower H', "HSV Tuner")
        upperH = cv2.getTrackbarPos('Higher H', "HSV Tuner")

        lowerS = cv2.getTrackbarPos('Lower S', "HSV Tuner")
        upperS = cv2.getTrackbarPos('Higher S', "HSV Tuner")

        lowerV = cv2.getTrackbarPos('Lower V', "HSV Tuner")
        upperV = cv2.getTrackbarPos('Higher V', "HSV Tuner")

        in_rgb = q_rgb.tryGet()
        if in_rgb is not None:
            frame = in_rgb.getCvFrame()
        if frame is not None:
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            lowerThreshold = np.array([lowerH, lowerS, lowerV])
            upperThreshold = np.array([upperH, upperS, upperV])

            #check if color in range
            mask = cv2.inRange(hsv, lowerThreshold, upperThreshold)

            result = cv2.bitwise_and(frame, frame, mask = mask)

            edges = cv2.Canny(mask, 75, 150)

            lines = cv2.HoughLinesP(edges, 10, np.pi/180, 2)

            numLines = 0

            if lines is not None:
                centerX = 0
                centerY = 0
                for i in range(0, len(lines)):
                    # print(lines[i])
                    l = lines[i][0]
                    # print("L1: " + str(l[0]) + "L2: " + str(l[2]))
                    cv2.line(frame, (l[0], l[1]), (l[2], l[3]), (0, 0, 255), 7, cv2.LINE_AA)
                    numLines = numLines + 1
                    centerX = centerX + l[0]
                    centerY = centerY + l[1]

            if numLines != 0:
                centerX = centerX/numLines
                centerY = centerY/numLines

            centerX = int(centerX)
            centerY = int(centerY)

            topLeft = depthai.Point2f((centerX/640) - 0.01, (centerY/400) - 0.01)
            bottomRight = depthai.Point2f((centerX/640) + 0.01, (centerY/400) + 0.01)

            config.roi = depthai.Rect(topLeft, bottomRight)
            cfg = depthai.SpatialLocationCalculatorConfig()
            cfg.addROI(config)
            spatialCalcConfigInQueue.send(cfg)

            angle = (centerX - 319.5) * (71.9/640)

            color = (255, 255, 255)

            if lines is not None:
                spatialData = inDepthAvg.getSpatialLocations()
                roi = spatialData[0].config.roi
                roi = roi.denormalize(width=depthFrameColor.shape[1], height=depthFrameColor.shape[0])
                xmin = int(roi.topLeft().x)
                ymin = int(roi.topLeft().y)
                xmax = int(roi.bottomRight().x)
                ymax = int(roi.bottomRight().y)

                cv2.circle(frame, (centerX, centerY), 3, color)
                cv2.rectangle(depthFrameColor, (xmin, ymin), (xmax, ymax), color, cv2.FONT_HERSHEY_SCRIPT_SIMPLEX)
                print("Z: " + str((spatialData[0].spatialCoordinates.z)/25.4) + " X: " + str((spatialData[0].spatialCoordinates.x)) + " Y: " + str((spatialData[0].spatialCoordinates.y)))

            # cv2.imshow("Disparity", disparity)
            cv2.imshow("depth", depthFrameColor)
            cv2.imshow("mask", result)
            cv2.imshow("RGB", frame)
        if cv2.waitKey(1) == ord('q'):
            break