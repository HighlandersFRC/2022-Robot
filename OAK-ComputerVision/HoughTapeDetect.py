import numpy as np  # numpy - manipulate the packet data returned by depthai
import cv2  # opencv - display the video stream
import depthai  # depthai - access the camera and its data packets

pipeline = depthai.Pipeline()

cam_rgb = pipeline.create(depthai.node.ColorCamera)
cam_rgb.setPreviewSize(500, 500)

xout_rgb = pipeline.create(depthai.node.XLinkOut)
xout_rgb.setStreamName("rgb")
cam_rgb.preview.link(xout_rgb.input)

controlIn = pipeline.create(depthai.node.XLinkIn)
controlIn.setStreamName('control')
controlIn.out.link(cam_rgb.inputControl)

lowerH = 57
upperH = 84

lowerS = 222
upperS = 255

lowerV = 62
upperV = 255

expTime = 2000
sensIso = 200

centerX = 0
centerY = 0
numLines = 0

focal_length_in_pixels = 882.5
distBetweenCameras = 2.95276

def getMonoCamera(pipeline, isLeft):
    # Configure mono camera
    mono = pipeline.createMonoCamera()
    # Set Camera Resolution
    mono.setResolution(depthai.MonoCameraProperties.SensorResolution.THE_400_P)
    if isLeft:
        # Get left camera
        mono.setBoardSocket(depthai.CameraBoardSocket.LEFT)
    else :
        # Get right camera
        mono.setBoardSocket(depthai.CameraBoardSocket.RIGHT)
    return mono

def getStereoPair(pipeline, monoleft, monoRight):
    stereo = pipeline.createStereoDepth()
    stereo.setLeftRightCheck(True)

    monoLeft.out.link(stereo.left)
    monoRight.out.link(stereo.right)

    return stereo

def on_change(value):
    print(value)

def getFrame(queue):
  # Get frame from queue
  frame = queue.get()
  # Convert frame to OpenCV format and return
  return frame.getCvFrame()

# Set up left and right cameras
monoLeft = getMonoCamera(pipeline, isLeft = True)
monoRight = getMonoCamera(pipeline, isLeft = False)

stereo = getStereoPair(pipeline, monoLeft, monoRight)

# Set output Xlink for left camera
xoutLeft = pipeline.createXLinkOut()
xoutLeft.setStreamName("left")

# Set output Xlink for right camera
xoutRight = pipeline.createXLinkOut()
xoutRight.setStreamName("right")

xoutDepth = pipeline.createXLinkOut()
xoutDepth.setStreamName("depth")

xoutDisp = pipeline.createXLinkOut()
xoutDisp.setStreamName("disparity")

stereo.disparity.link(xoutDisp.input)

# Attach cameras to output Xlink
monoLeft.out.link(xoutLeft.input)
monoRight.out.link(xoutRight.input)

with depthai.Device(pipeline) as device:
    q_rgb = device.getOutputQueue("rgb")
    frame = None

    disparityQueue = device.getOutputQueue(name = "disparity", maxSize = 1, blocking = False)

    disparityMultiplier = 255/(stereo.getMaxDisparity())

    leftQueue = device.getOutputQueue(name="left", maxSize=1)
    rightQueue = device.getOutputQueue(name="right", maxSize=1)

    # cv2.namedWindow("Stereo Pair")

    cv2.namedWindow('HSV Tuner', cv2.WINDOW_AUTOSIZE)
    
    cv2.createTrackbar('Lower H', "HSV Tuner", 0, 255, on_change)
    cv2.createTrackbar('Higher H', "HSV Tuner", 0, 255, on_change)
    cv2.createTrackbar('Lower S', "HSV Tuner", 0, 255, on_change)
    cv2.createTrackbar('Higher S', "HSV Tuner", 0, 255, on_change)
    cv2.createTrackbar('Lower V', "HSV Tuner", 0, 255, on_change)
    cv2.createTrackbar('Higher V', "HSV Tuner", 0, 255, on_change)

    while True:
        # print(lowerH)

        # Get left frame
        leftFrame = getFrame(leftQueue)
        # Get right frame 
        rightFrame = getFrame(rightQueue)

        disparity = getFrame(disparityQueue)

        disparity = (disparity * disparityMultiplier).astype(np.uint8)
        distance = focal_length_in_pixels * distBetweenCameras/ disparity
        print((distance))
        disparity = cv2.applyColorMap(disparity, cv2.COLORMAP_JET)


        # imOut = np.hstack((leftFrame, rightFrame))
        imOut = np.uint8(leftFrame/2 + rightFrame/2)

        lowerH = cv2.getTrackbarPos('Lower H', "HSV Tuner")
        upperH = cv2.getTrackbarPos('Higher H', "HSV Tuner")

        lowerS = cv2.getTrackbarPos('Lower S', "HSV Tuner")
        upperS = cv2.getTrackbarPos('Higher S', "HSV Tuner")

        lowerV = cv2.getTrackbarPos('Lower V', "HSV Tuner")
        upperV = cv2.getTrackbarPos('Higher V', "HSV Tuner")

        in_rgb = q_rgb.tryGet()
        controlQueue = device.getInputQueue('control')
        ctrl = depthai.CameraControl()
        ctrl.setManualExposure(expTime, sensIso)
        controlQueue.send(ctrl)
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

            lines = cv2.HoughLinesP(edges,1,np.pi/180,10)

            numLines = 0

            if lines is not None:
                for i in range(0, len(lines)):
                    l = lines[i][0]
                    cv2.line(frame, (l[0], l[1]), (l[2], l[3]), (0, 0, 255), 5, cv2.LINE_AA)
                    numLines = numLines + 2
                    centerX = centerX + l[0] + l[2]
                    centerY = centerY + l[1] + l[3]

            if numLines != 0:
                centerX = centerX/numLines
                centerY = centerY/numLines

            centerX = int(centerX)
            centerY = int(centerY)

            # print("CenterX: " + str(centerX) + " CenterY: " + str(centerY))

            cv2.circle(frame, (centerX, centerY), 15, (120, 255, 255))

            cv2.imshow("Disparity", disparity)
            cv2.imshow("mask", result)
            cv2.imshow("RGB", frame)
        if cv2.waitKey(1) == ord('q'):
            break