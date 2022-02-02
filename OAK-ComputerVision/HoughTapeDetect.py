# import numpy as np  # numpy - manipulate the packet data returned by depthai
# import cv2  # opencv - display the video stream
# import depthai  # depthai - access the camera and its data packets
# import math
# from paho.mqtt import client as mqtt_client

# broker = '10.44.99.11'
# port = 1883
# pubTopic = "/sensors/camera"
# subTopic = "/robot/camera"
# client_id = "44H99"

# sub_client_id = "99H44"

# def connect_mqtt():
#     def on_connect(client, userdata, flags, rc):
#         if rc == 0:
#             print("Connected to MQTT Broker!")
#         else:
#             print("Failed to connect, return code %d\n", rc)
#     # Set Connecting Client ID
#     client = mqtt_client.Client(client_id)
#     client.username_pw_set("4499", "4499")
#     client.on_connect = on_connect
#     client.connect(broker, port)
#     return client

# def connect_mqttSub():
#     def on_connect(client, userdata, flags, rc):
#         if rc == 0:
#            print("Connected to MQTT Broker!")
#         else:
#            print("Failed to connect, return code %d\n", rc)
#         #Set Connecting Client ID
#     client = mqtt_client.Client(sub_client_id)
#     client.username_pw_set("4499", "4499")
#     client.on_connect = on_connect
#     client.connect(broker)
#     return client

# def publish(client, msg):
#     msg_count = 0
#     result = client.publish(pubTopic, msg)
#     # result: [0, 1]
#     status = result[0]
#     if(status != 0):
#         print("Failed to send message to Topic")
#     msg_count += 1

# def subscribe(client):
#     def on_message(client, userdata, msg):
#         print("Received " + str(msg) + " from Topic " + str(subTopic))

#     # print("Listening")
#     client.subscribe(subTopic, 2)
#     client.on_message = on_message

# pipeline = depthai.Pipeline()

# imu = pipeline.create(depthai.node.IMU)
# xlinkOut = pipeline.create(depthai.node.XLinkOut)

# xlinkOut.setStreamName("imu")

# imu.enableIMUSensor(depthai.IMUSensor.ROTATION_VECTOR, 400)

# imu.setBatchReportThreshold(1)

# imu.setMaxBatchReports(10)

# imu.out.link(xlinkOut.input)

# cam_rgb = pipeline.create(depthai.node.ColorCamera)
# cam_rgb.setPreviewSize(640, 400)

# xout_rgb = pipeline.create(depthai.node.XLinkOut)
# xout_rgb.setStreamName("rgb")
# cam_rgb.preview.link(xout_rgb.input)

# xinSpatialCalcConfig = pipeline.createXLinkIn()
# xinSpatialCalcConfig.setStreamName("spatialCalcConfig")

# controlIn = pipeline.create(depthai.node.XLinkIn)
# controlIn.setStreamName('control')
# controlIn.out.link(cam_rgb.inputControl)

# spatialLocationCalculator = pipeline.createSpatialLocationCalculator()

# lowerH = 35
# upperH = 82

# lowerS = 173
# upperS = 255

# lowerV = 63
# upperV = 245

# expTime = 1200
# sensIso = 200

# centerX = 0
# centerY = 0
# numLines = 0

# focal_length_in_pixels = 640 * 0.5 / math.tan(71.9 * 0.5 * math.pi / 180)
# distBetweenCameras = 7.5

# def getMonoCamera(pipeline, isLeft):
#     # Configure mono camera
#     mono = pipeline.createMonoCamera()
#     # Set Camera Resolution
#     mono.setResolution(depthai.MonoCameraProperties.SensorResolution.THE_400_P)
#     # mono.setPreviewSize(400, 400)
#     if isLeft:
#     # Get left camera
#         mono.setBoardSocket(depthai.CameraBoardSocket.LEFT)
#     else :
#     # Get right camera
#         mono.setBoardSocket(depthai.CameraBoardSocket.RIGHT)
#     return mono

# def getStereoPair(pipeline, monoLeftCam, monoRightCam):
#     stereo = pipeline.createStereoDepth()
#     # stereo.setLeftRightCheck(True)
#     stereo.setSubpixel(False)

#     monoLeftCam.out.link(stereo.left)
#     monoRightCam.out.link(stereo.right)

#     return stereo

# def on_change(value):
#     print(value)

# def getFrame(queue):
#     # Get frame from queue
#     frame = queue.get()
#     # Convert frame to OpenCV format and return
#     return frame.getCvFrame()

# # Set up left and right cameras
# monoLeft = pipeline.createMonoCamera()
# monoRight = pipeline.createMonoCamera()
# stereo = pipeline.createStereoDepth()

# stereo.setOutputDepth(True)
# stereo.setOutputRectified(False)
# stereo.setConfidenceThreshold(255)
# stereo.setLeftRightCheck(False)
# stereo.setSubpixel(False)

# monoLeft.setResolution(depthai.MonoCameraProperties.SensorResolution.THE_400_P)
# monoLeft.setBoardSocket(depthai.CameraBoardSocket.LEFT)
# monoRight.setResolution(depthai.MonoCameraProperties.SensorResolution.THE_400_P)
# monoRight.setBoardSocket(depthai.CameraBoardSocket.RIGHT)

# monoLeft.out.link(stereo.left)
# monoRight.out.link(stereo.right)

# spatialLocationCalculator = pipeline.createSpatialLocationCalculator()
# xoutSpatialData = pipeline.createXLinkOut()
# xinSpatialCalcConfig = pipeline.createXLinkIn()

# xoutDepth = pipeline.createXLinkOut()
# xoutDepth.setStreamName("depth")

# spatialLocationCalculator.passthroughDepth.link(xoutDepth.input)
# stereo.depth.link(spatialLocationCalculator.inputDepth)

# topLeft = depthai.Point2f(0.1, 0.1)
# bottomRight = depthai.Point2f(0.2, 0.2)

# spatialLocationCalculator.setWaitForConfigInput(False)
# config = depthai.SpatialLocationCalculatorConfigData()
# config.depthThresholds.lowerThreshold = 100
# config.depthThresholds.upperThreshold = 10000
# config.roi = depthai.Rect(topLeft, bottomRight)
# spatialLocationCalculator.initialConfig.addROI(config)
# spatialLocationCalculator.out.link(xoutSpatialData.input)
# xinSpatialCalcConfig.out.link(spatialLocationCalculator.inputConfig)

# xoutSpatialData.setStreamName("spatialData")
# xinSpatialCalcConfig.setStreamName("spatialCalcConfig")

# # with depthai.Device(pipeline) as device:
# #     q_rgb = device.getOutputQueue("rgb")
# #     frame = None

#     # client = connect_mqtt()
#     # subClient = connect_mqttSub()

#     # subClient.loop_start()


#     # imuQueue = device.getOutputQueue(name="imu", maxSize=50, blocking = False)

#     # baseTs = None

#     depthQueue = device.getOutputQueue("depth", maxSize=4, blocking=False)
#     spatialCalcQueue = device.getOutputQueue(name="spatialData", maxSize=4, blocking=False)
#     spatialCalcConfigInQueue = device.getInputQueue("spatialCalcConfig")

#     # cv2.namedWindow('HSV Tuner', cv2.WINDOW_AUTOSIZE)

#     # cv2.createTrackbar('Lower H', "HSV Tuner", 0, 255, on_change)
#     # cv2.createTrackbar('Higher H', "HSV Tuner", 0, 255, on_change)
#     # cv2.createTrackbar('Lower S', "HSV Tuner", 0, 255, on_change)
#     # cv2.createTrackbar('Higher S', "HSV Tuner", 0, 255, on_change)
#     # cv2.createTrackbar('Lower V', "HSV Tuner", 0, 255, on_change)
#     # cv2.createTrackbar('Higher V', "HSV Tuner", 0, 255, on_change)

#     # cv2.setTrackbarPos('Lower H', "HSV Tuner", lowerH)
#     # cv2.setTrackbarPos('Higher H', "HSV Tuner", upperH)
#     # cv2.setTrackbarPos('Lower S', "HSV Tuner", lowerS)
#     # cv2.setTrackbarPos('Higher S', "HSV Tuner", upperS)
#     # cv2.setTrackbarPos('Lower V', "HSV Tuner", lowerV)
#     # cv2.setTrackbarPos('Higher V', "HSV Tuner", upperV)

# while True:
#     # controlQueue = device.getInputQueue('control')
#     # ctrl = depthai.CameraControl()
#     # ctrl.setManualExposure(expTime, sensIso)
#     # controlQueue.send(ctrl)

#     # imuData = imuQueue.get()

#     # imuPackets = imuData.packets

#     # for imuPacket in imuPackets:
#     #     rVvalues = imuPacket.rotationVector

#     #     rvTs = rVvalues.timestamp.get()

#     #     if baseTs is None:
#     #         baseTs = rvTs
#     #     rvTs = rvTs - baseTs

#     #     imuF = "{:.06f}"
#     #     tsF = "{:.03f}"

#     #     # print(f"Quaternion: i: {imuF.format(rVvalues.i)} j: {imuF.format(rVvalues.j)}" f"k: {imuF.format(rVvalues.k)} real: {imuF.format(rVvalues.real)}")

#     # iVal = float(imuF.format(rVvalues.i))
#     # jVal = float(imuF.format(rVvalues.j))
#     # kVal = float(imuF.format(rVvalues.k))
#     # realVal = float(imuF.format(rVvalues.real))

#     # cameraRollAngle = 2 * math.acos(realVal)

#     # cameraXVector = (iVal/(math.sin(cameraRollAngle/2)))
#     # cameraYVector = (jVal/(math.sin(cameraRollAngle/2)))
#     # cameraZVector = (kVal/(math.sin(cameraRollAngle/2)))

#     # camAngleToTarget = 2 * math.degrees(math.atan((cameraZVector)/(math.sqrt((cameraXVector ** 2) + (cameraYVector ** 2)))))

#     inDepth = depthQueue.get() # blocking call, will wait until a new data has arrived
#     inDepthAvg = spatialCalcQueue.get() # blocking call, will wait until a new data has arrived

#     depthFrame = inDepth.getFrame()
#     depthFrameColor = cv2.normalize(depthFrame, None, 255, 0, cv2.NORM_MINMAX, cv2.CV_8UC1)
#     depthFrameColor = cv2.equalizeHist(depthFrameColor)
#     depthFrameColor = cv2.applyColorMap(depthFrameColor, cv2.COLORMAP_JET)

#     # lowerH = cv2.getTrackbarPos('Lower H', "HSV Tuner")
#     # upperH = cv2.getTrackbarPos('Higher H', "HSV Tuner")

#     # lowerS = cv2.getTrackbarPos('Lower S', "HSV Tuner")
#     # upperS = cv2.getTrackbarPos('Higher S', "HSV Tuner")

#     # lowerV = cv2.getTrackbarPos('Lower V', "HSV Tuner")
#     # upperV = cv2.getTrackbarPos('Higher V', "HSV Tuner")

#     # in_rgb = q_rgb.tryGet()
#     # if in_rgb is not None:
#     #     frame = in_rgb.getCvFrame()
#     # if frame is not None:
#         # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

#         # lowerThreshold = np.array([lowerH, lowerS, lowerV])
#         # upperThreshold = np.array([upperH, upperS, upperV])

#         # #check if color in range
#         # mask = cv2.inRange(hsv, lowerThreshold, upperThreshold)

#         # result = cv2.bitwise_and(frame, frame, mask = mask)

#         # edges = cv2.Canny(mask, 75, 150)

#         # contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

#         # print(type(contours))
#         # for contour in contours:
#         #     peri = cv2.arcLength(contour, True)
#         #     approx = cv2.approxPolyDP(contour, 0.04 * peri, True)
#         #     cntArea = cv2.contourArea(contour)
#         #     rotatedRect = cv2.minAreaRect(contour)
#         #     box = cv2.boxPoints(rotatedRect)
#         #     boxArray = np.int0(box)
#         #     topLeftX = boxArray[0][0]
#         #     topLeftY = boxArray[0][1]
#         #     bottomRightX = boxArray[1][0]
#         #     bottomRightY = boxArray[1][1]
#         #     boxColor = (0,0,255)

#         #     cv2.drawContours(frame,[boxArray],0,boxColor,2)


#     topLeft = depthai.Point2f(0.9, 0.9)
#     bottomRight = depthai.Point2f(0.95, 0.95)

#     config.roi = depthai.Rect(topLeft, bottomRight)
#     cfg = depthai.SpatialLocationCalculatorConfig()
#     cfg.addROI(config)
#     print(cfg)
#     spatialCalcConfigInQueue.send(cfg)

#     spatialData = inDepthAvg.getSpatialLocations()
#     roi = spatialData[0].config.roi
#     roi = roi.denormalize(width=depthFrameColor.shape[1], height=depthFrameColor.shape[0])
#     xmin = int(roi.topLeft().x)
#     ymin = int(roi.topLeft().y)
#     xmax = int(roi.bottomRight().x)
#     ymax = int(roi.bottomRight().y)

#     cv2.rectangle(depthFrameColor, (xmin, ymin), (xmax, ymax), (0, 0, 0), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX)

#         # config.roi = depthai.Rect(topLeft, bottomRight)
#         # cfg = depthai.SpatialLocationCalculatorConfig()
#         # cfg.addROI(config)
#         # spatialCalcConfigInQueue.send(cfg)

        

#         # print("Z: " + str((spatialData[0].spatialCoordinates.z)/25.4) + " X: " + str((spatialData[0].spatialCoordinates.x)) + " Y: " + str((spatialData[0].spatialCoordinates.y)))




#         # lines = cv2.HoughLinesP(edges, 5, np.pi/180, 2)

#         # numLines = 0

#         # if lines is not None:
#         #     centerX = 0
#         #     centerY = 0
#         #     for i in range(0, len(lines)):
#         #         # print(lines[i])
#         #         l = lines[i][0]
#         #         # print("L1: " + str(l[0]) + "L2: " + str(l[2]))
#         #         cv2.line(frame, (l[0], l[1]), (l[2], l[3]), (0, 0, 255), 2, cv2.LINE_AA)
#         #         numLines = numLines + 1
#         #         centerX = centerX + l[0]
#         #         centerY = centerY + l[1]

#         # if numLines != 0:
#         #     centerX = centerX/numLines
#         #     centerY = centerY/numLines

#         # centerX = int(centerX)
#         # centerY = int(centerY)

#         # topLeft = depthai.Point2f((centerX/640) - 0.01, (centerY/400) - 0.01)
#         # bottomRight = depthai.Point2f((centerX/640) + 0.01, (centerY/400) + 0.01)

#         # config.roi = depthai.Rect(topLeft, bottomRight)
#         # cfg = depthai.SpatialLocationCalculatorConfig()
#         # cfg.addROI(config)
#         # spatialCalcConfigInQueue.send(cfg)

#         # angleArray = []
#         # distanceArray = []

#         # if lines is not None:
#         #     for line in lines:
#         #         centerX = (line[0])
#         #         angle = (centerX - 319.5) * (71.9/640)
#         #         angleArray.append(angle)
#         # print(angleArray)                    


#         # color = (255, 255, 255)

#         # if lines is not None:
#         #     spatialData = inDepthAvg.getSpatialLocations()
#         #     roi = spatialData[0].config.roi
#         #     roi = roi.denormalize(width=depthFrameColor.shape[1], height=depthFrameColor.shape[0])
#         #     xmin = int(roi.topLeft().x)
#         #     ymin = int(roi.topLeft().y)
#         #     xmax = int(roi.bottomRight().x)
#         #     ymax = int(roi.bottomRight().y)

#             # cv2.circle(frame, (centerX, centerY), 3, color)
#             # cv2.rectangle(depthFrameColor, (xmin, ymin), (xmax, ymax), color, cv2.FONT_HERSHEY_SCRIPT_SIMPLEX)

#             # JSONString = '{"Distance": ' + str(centerX) + ', "Angle":' + str(angle) + '}' 

#             # publish(client, JSONString)
#             # print("Z: " + str((spatialData[0].spatialCoordinates.z)/25.4) + " X: " + str((spatialData[0].spatialCoordinates.x)) + " Y: " + str((spatialData[0].spatialCoordinates.y)))
        
#         # publish(client, "Hola")
#         # subscribe(subClient)
#         # client.loop_forever()

#         # print("Running")

#         # cv2.imshow("Disparity", disparity)
#         # cv2.imshow("Contours", edges)
#     cv2.imshow("depth", depthFrameColor)
#         # cv2.imshow("mask", result)
#         # cv2.imshow("RGB", frame)
#     if cv2.waitKey(1) == ord('q'):
#         break

#!/usr/bin/env python3

import cv2
import depthai
import numpy as np  # numpy - manipulate the packet data returned by depthai
import math
from math import cos, sin, tan, pi

broker = '10.44.99.11'
port = 1883
pubTopic = "/sensors/camera"
subTopic = "/robot/camera"
client_id = "44H99"

sub_client_id = "99H44"

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)
    client.username_pw_set("4499", "4499")
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def connect_mqttSub():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
           print("Connected to MQTT Broker!")
        else:
           print("Failed to connect, return code %d\n", rc)
        #Set Connecting Client ID
    client = mqtt_client.Client(sub_client_id)
    client.username_pw_set("4499", "4499")
    client.on_connect = on_connect
    client.connect(broker)
    return client

def publish(client, msg):
    msg_count = 0
    result = client.publish(pubTopic, msg)
    # result: [0, 1]
    status = result[0]
    if(status != 0):
        print("Failed to send message to Topic")
    msg_count += 1

def subscribe(client):
    def on_message(client, userdata, msg):
        print("Received " + str(msg) + " from Topic " + str(subTopic))

    # print("Listening")
    client.subscribe(subTopic, 2)
    client.on_message = on_message

def on_change(value):
    print(value)

def getRotX(theta):
	return np.array([
		[1,0,0,0],
		[0,cos(theta),-sin(theta),0],
		[0,sin(theta),cos(theta),0],
		[0,0,0,1],
	])
def getRotY(theta):
	return np.array([
		[cos(theta),0,-sin(theta),0],
		[0,1,0,0],
		[-sin(theta),cos(theta),0,0],
		[0,0,0,1],
	])
def getRotZ(theta):
	return np.array([
		[cos(theta),-sin(theta),0,0],
		[sin(theta),cos(theta),0,0],
		[0,0,1,0],
		[0,0,0,1],
	])
def leftRightFlip():
	return np.array([
		[-1,0,0,0],
		[0,1,0,0],
		[0,0,1,0],
		[0,0,0,1]
	])

def getCircleOfBestFitCenter(xList, yList):
    inputList = []
    dList = []
    for i in range(0, len(xList)):
        inputList.append([xList[i], yList[i], 1])
        dList.append([(xList[i] ** 2) + (yList[i] ** 2)])
    
    inputMatrix = np.array(inputList)
    dMatrix = np.array(dList)

    outputMatrix = (np.linalg.pinv(inputMatrix)) @ dMatrix

    xCenter = outputMatrix[0]/2
    yCenter = outputMatrix[1]/2

    rSquared = outputMatrix[2] - (xCenter ** 2) - (yCenter ** 2)
    centers = [[xCenter, yCenter, rSquared]]

    return centers 


def convertCoordinates(x, y, z):
    input_point = np.array([x, y, z, 1]).T
    transform = getRotZ(pi/2) @ getRotX(pi/2 - cameraElevation) @ leftRightFlip()
    mapped_point = transform @ input_point
    # print(input_point)
    # print(mapped_point)
    return mapped_point

def updateHSV():
    lowerH = cv2.getTrackbarPos('Lower H', "HSV Tuner")
    upperH = cv2.getTrackbarPos('Higher H', "HSV Tuner")

    lowerS = cv2.getTrackbarPos('Lower S', "HSV Tuner")
    upperS = cv2.getTrackbarPos('Higher S', "HSV Tuner")

    lowerV = cv2.getTrackbarPos('Lower V', "HSV Tuner")
    upperV = cv2.getTrackbarPos('Higher V', "HSV Tuner")

### NOT WORKING ###
def getImuAngle(): 
    imuData = imuQueue.get()

    baseTs = None

    imuPackets = imuData.packets

    for imuPacket in imuPackets:
        # print(imuPacket)

        rVvalues = imuPacket.rotationVector

        rvTs = rVvalues.timestamp.get()

        if baseTs is None:
            baseTs = rvTs
        rvTs = rvTs - baseTs

        imuF = "{:.06f}"
        tsF = "{:.03f}"

        # print(f"Quaternion: i: {imuF.format(rVvalues.i)} j: {imuF.format(rVvalues.j)}" f"k: {imuF.format(rVvalues.k)} real: {imuF.format(rVvalues.real)}")

    iVal = float(imuF.format(rVvalues.i))
    jVal = float(imuF.format(rVvalues.j))
    kVal = float(imuF.format(rVvalues.k))
    realVal = float(imuF.format(rVvalues.real))

    cameraRollAngle = 2 * math.acos(realVal)

    cameraXVector = (iVal/(math.sin(cameraRollAngle/2)))
    cameraYVector = (jVal/(math.sin(cameraRollAngle/2)))
    cameraZVector = (kVal/(math.sin(cameraRollAngle/2)))

    camAngleToTarget = 2 * math.degrees(math.atan((cameraZVector)/(math.sqrt((cameraXVector ** 2) + (cameraYVector ** 2)))))

    print("X: " + str(cameraXVector) + " Y: " + str(cameraYVector) + " Z: " + str(cameraZVector))
# 
    # print("X: " + str(angle.x * 180/math.pi) + "Y: " + str(angle.y * 180/math.pi) + "Z: " + str(angle.z * 180/math.pi))

stepSize = 0.05

cameraResolutionWidth = 1280
cameraResolutionHeight = 720

# Camera elevation from horizontal, remember to change
cameraElevation = 0 * pi/180.0

targetHeightDifference = 92

# Start defining a pipeline
pipeline = depthai.Pipeline()

cam_rgb = pipeline.create(depthai.node.ColorCamera)
cam_rgb.setPreviewSize(640, 480)
cam_rgb.setResolution(depthai.ColorCameraProperties.SensorResolution.THE_1080_P)
cam_rgb.setIspScale(2, 3)
# cam_rgb.setPreviewSize(cameraResolutionWidth, cameraResolutionHeight)

xout_rgb = pipeline.create(depthai.node.XLinkOut)
xout_rgb.setStreamName("rgb")
cam_rgb.preview.link(xout_rgb.input)

controlIn = pipeline.create(depthai.node.XLinkIn)
controlIn.setStreamName('control')
controlIn.out.link(cam_rgb.inputControl)

lowerH = 49
upperH = 77

lowerS = 223
upperS = 255

lowerV = 19
upperV = 117

expTime = 1000
sensIso = 500

# Define a source - two mono (grayscale) cameras
monoLeft = pipeline.createMonoCamera()
monoRight = pipeline.createMonoCamera()
stereo = pipeline.createStereoDepth()
spatialLocationCalculator = pipeline.createSpatialLocationCalculator()

xoutDepth = pipeline.createXLinkOut()
xoutSpatialData = pipeline.createXLinkOut()
xinSpatialCalcConfig = pipeline.createXLinkIn()

xoutDepth.setStreamName("depth")
xoutSpatialData.setStreamName("spatialData")
xinSpatialCalcConfig.setStreamName("spatialCalcConfig")

# MonoCamera
monoLeft.setResolution(depthai.MonoCameraProperties.SensorResolution.THE_400_P)
monoLeft.setBoardSocket(depthai.CameraBoardSocket.LEFT)
monoRight.setResolution(depthai.MonoCameraProperties.SensorResolution.THE_400_P)
monoRight.setBoardSocket(depthai.CameraBoardSocket.RIGHT)

outputDepth = True
outputRectified = False
lrcheck = True
subpixel = False

# StereoDepth
stereo.setOutputDepth(outputDepth)
stereo.setOutputRectified(outputRectified)
stereo.setConfidenceThreshold(255)
stereo.setDepthAlign(depthai.CameraBoardSocket.RGB)
stereo.setOutputSize(640, 480)

stereo.setLeftRightCheck(lrcheck)
stereo.setSubpixel(subpixel)

monoLeft.out.link(stereo.left)
monoRight.out.link(stereo.right)

spatialLocationCalculator.passthroughDepth.link(xoutDepth.input)
stereo.depth.link(spatialLocationCalculator.inputDepth)

topLeft = depthai.Point2f(0.4, 0.4)
bottomRight = depthai.Point2f(0.6, 0.6)

spatialLocationCalculator.setWaitForConfigInput(False)
config = depthai.SpatialLocationCalculatorConfigData()
config.depthThresholds.lowerThreshold = 100
config.depthThresholds.upperThreshold = 10000
config.roi = depthai.Rect(topLeft, bottomRight)
spatialLocationCalculator.initialConfig.addROI(config)
spatialLocationCalculator.out.link(xoutSpatialData.input)
xinSpatialCalcConfig.out.link(spatialLocationCalculator.inputConfig)

imu = pipeline.create(depthai.node.IMU)
xlinkOut = pipeline.create(depthai.node.XLinkOut)

xlinkOut.setStreamName("imu")

# imu.enableIMUSensor(depthai.IMUSensor.ROTATION_VECTOR, 400)
imu.enableIMUSensor(depthai.IMUSensor.GAME_ROTATION_VECTOR, 400)

imu.setBatchReportThreshold(1)

imu.setMaxBatchReports(10)

imu.out.link(xlinkOut.input)

# Pipeline defined, now the device is assigned and pipeline is started
device = depthai.Device(pipeline)
device.startPipeline()

imuQueue = device.getOutputQueue(name="imu", maxSize=50, blocking = False)

# Output queue will be used to get the depth frames from the outputs defined above
depthQueue = device.getOutputQueue(name="depth", maxSize=4, blocking=False)
spatialCalcQueue = device.getOutputQueue(name="spatialData", maxSize=4, blocking=False)
spatialCalcConfigInQueue = device.getInputQueue("spatialCalcConfig")

color = (255, 255, 255)

q_rgb = device.getOutputQueue("rgb")
frame = None

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

# transformationMatrix = getTransform(cameraElevation)

# adjustedCoordinates = convertCoordinates(0, 1, 1)
# adjustedCoordinates[2][0] = -adjustedCoordinates[2][0]

# print(adjustedCoordinates)

# xList = [0, 17, -23, 13]
# yList = [75, 73.3, 70.328, 74.111]

# targetCenter = getCircleOfBestFitCenter(xList, yList)
# targetCenterX = targetCenter[0][0]
# # print(targetCenterX)
# targetCenterY = targetCenter[0][1]
# targetRadiusCheck = targetCenter[0][2]

# print("X: " + str(targetCenterX) + " Y: " + str(targetCenterY) + " R: " + str(targetRadiusCheck))

while True:
    controlQueue = device.getInputQueue('control')
    ctrl = depthai.CameraControl()
    ctrl.setManualExposure(expTime, sensIso)
    controlQueue.send(ctrl)

    lowerH = cv2.getTrackbarPos('Lower H', "HSV Tuner")
    upperH = cv2.getTrackbarPos('Higher H', "HSV Tuner")

    lowerS = cv2.getTrackbarPos('Lower S', "HSV Tuner")
    upperS = cv2.getTrackbarPos('Higher S', "HSV Tuner")

    lowerV = cv2.getTrackbarPos('Lower V', "HSV Tuner")
    upperV = cv2.getTrackbarPos('Higher V', "HSV Tuner")
    # getImuAngle()

    inDepth = depthQueue.get() # blocking call, will wait until a new data has arrived
    inDepthAvg = spatialCalcQueue.get() # blocking call, will wait until a new data has arrived
    
    depthFrame = inDepth.getFrame()
    depthFrameColor = cv2.normalize(depthFrame, None, 255, 0, cv2.NORM_INF, cv2.CV_8UC1)
    depthFrameColor = cv2.equalizeHist(depthFrameColor)
    depthFrameColor = cv2.applyColorMap(depthFrameColor, cv2.COLORMAP_OCEAN)

    in_rgb = q_rgb.tryGet()
    if in_rgb is not None:
        frame = in_rgb.getCvFrame()
        # print(frame.size)
    if frame is not None:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lowerThreshold = np.array([lowerH, lowerS, lowerV])
        upperThreshold = np.array([upperH, upperS, upperV])

        #check if color in range
        mask = cv2.inRange(hsv, lowerThreshold, upperThreshold)

        result = cv2.bitwise_and(frame, frame, mask = mask)

        edges = cv2.Canny(mask, 75, 150)

        contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        zList = []
        xList = []
        yList = []

        for contour in contours:
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.04 * peri, True)
            rotatedRect = cv2.minAreaRect(contour)
            box = cv2.boxPoints(rotatedRect)
            boxArray = np.int0(box)
            topLeftX = boxArray[0][0]
            topLeftY = boxArray[0][1]
            bottomRightX = boxArray[1][0]
            bottomRightY = boxArray[1][1]
            boxColor = (0,0,255)

            # cv2.drawContours(depthFrameColor,[boxArray],0,boxColor,2)
            cv2.drawContours(frame,[boxArray],0,boxColor,2)

            topLeft = depthai.Point2f((topLeftX/cameraResolutionWidth), (topLeftY/cameraResolutionHeight))
            bottomRight = depthai.Point2f((bottomRightX/cameraResolutionWidth), (bottomRightY/cameraResolutionHeight))

            config.roi = depthai.Rect(topLeft, bottomRight)
            cfg = depthai.SpatialLocationCalculatorConfig()
            cfg.addROI(config)
            # print(cfg)
            spatialCalcConfigInQueue.send(cfg)

            spatialData = inDepthAvg.getSpatialLocations()
            roi = spatialData[0].config.roi
            roi = roi.denormalize(width=depthFrameColor.shape[1], height=depthFrameColor.shape[0])
            xmin = int(roi.topLeft().x)
            ymin = int(roi.topLeft().y)
            xmax = int(roi.bottomRight().x)
            ymax = int(roi.bottomRight().y)

            cv2.rectangle(depthFrameColor, (xmin, ymin), (xmax, ymax), (0, 0, 0), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX)

            spatialData = inDepthAvg.getSpatialLocations()
            index = 0
            for depthData in spatialData:
                index += 1
                # print(index)
                print(len(depthData.spatialCoordinates.z))
                roi = depthData.config.roi
                roi = roi.denormalize(width=depthFrameColor.shape[1], height=depthFrameColor.shape[0])
                xmin = int(roi.topLeft().x)
                ymin = int(roi.topLeft().y)
                xmax = int(roi.bottomRight().x)
                ymax = int(roi.bottomRight().y)

                zCoordinateCamera = (depthData.spatialCoordinates.z)/25.4
                yCoordinateCamera = (depthData.spatialCoordinates.y)/25.4
                xCoordinateCamera = (depthData.spatialCoordinates.x)/25.4

                convertedCoordinates = convertCoordinates(xCoordinateCamera, yCoordinateCamera, zCoordinateCamera)

                # print("XRAW: " + str(xCoordinateCamera) + " Y: " + str(yCoordinateCamera) + " Z: " + str(zCoordinateCamera))

                # print("X: " + str(convertedCoordinates[0]) + " Y: " + str(convertedCoordinates[1]) + " Z: " + str(convertedCoordinates[2]))

                if(convertedCoordinates[2] != 0):
                    # print(str(convertedCoordinates[0]))
                    zList.append(convertedCoordinates[2])
                    xList.append(convertedCoordinates[0])
                    yList.append(convertedCoordinates[1])

                fontType = cv2.FONT_HERSHEY_TRIPLEX
                cv2.rectangle(depthFrameColor, (xmin, ymin), (xmax, ymax), color, cv2.FONT_HERSHEY_SCRIPT_SIMPLEX)
                cv2.putText(depthFrameColor, f"X: {int(depthData.spatialCoordinates.x)} mm", (xmin + 10, ymin + 20), fontType, 0.5, color)
                cv2.putText(depthFrameColor, f"Y: {int(depthData.spatialCoordinates.y)} mm", (xmin + 10, ymin + 35), fontType, 0.5, color)
                cv2.putText(depthFrameColor, f"Z: {int(depthData.spatialCoordinates.z)} mm", (xmin + 10, ymin + 50), fontType, 0.5, color)

        zMedian = np.median(zList)

        for i in range(0, len(zList)):
            if(abs(zList[i] - zMedian) >= 20):
                zList.remove(zList[i])
                xList.remove(xList[i])
                yList.remove(yList[i])

        # for i in range(0, len(zList)):
        #     factor = targetHeightDifference/zList[i]
        #     zList[i] = zList[i] * factor
        #     # xList[i] = xList[i] * factor
        #     # yList[i] = yList[i] * factor

        if(len(zList) != 0):
            targetCenter = getCircleOfBestFitCenter(xList, yList)
            targetCenterX = targetCenter[0][0]
            targetCenterY = targetCenter[0][1]
            targetRadiusCheck = targetCenter[0][2]

            # if(abs(targetRadiusCheck - 576) > 100):
            #     print("Didn't get correct target")
            # else:
            # print("CenterX: " + str(targetCenterX) + "CenterY: " + str(targetCenterY))

        # print(xList)

        cv2.imshow("depth", depthFrameColor)
        cv2.imshow("frame", frame)
        cv2.imshow("mask", result)

    # newConfig = False
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
