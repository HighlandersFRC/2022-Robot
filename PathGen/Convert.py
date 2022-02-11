import math
from datetime import datetime

def degreesToRadians(degrees):
    return degrees * (math.pi / 180)

def radiansToDegrees(radians):
    return radians * (180 / math.pi)

def getFieldPos(mousePos):
    mousePos = list(mousePos)

    x = mousePos[0]
    y = mousePos[1]

    x = (x - 150) * (16.4592 / 899)
    y = (-1 * (y - 472)) * (16.4592 / 899)


    return list((x, y))

def getPixelPos(point):
    point = list(point)

    pixelX = (point[0] / (16.4592 / 899)) + 150
    pixelY = -1 * (point[1] / (16.4592 / 899)) + 472

    pixelPos = (pixelX, pixelY)

    return pixelPos

def getDist(x1, y1, x2, y2):
    return math.sqrt( ( (x1 - x2) * (x1 - x2) ) + ( (y1 - y2) * (y1 - y2) ) )

def getDistPoints(point1, point2):
    x1 = list(point1)[0]
    y1 = list(point1)[1]
    x2 = list(point2)[0]
    y2 = list(point2)[1]

    return math.sqrt( ( (x1 - x2) * (x1 - x2) ) + ( (y1 - y2) * (y1 - y2) ) )

def getXY(r, theta, offsetX, offsetY):
    x = offsetX + r * math.cos(theta)
    y = offsetY + r * math.sin(theta)
    return (x, y)

def getTheta(x, y, offsetX, offsetY):
    theta = (math.pi / 2) - math.atan2(x - offsetX, y - offsetY)
    return theta

def round(num, places):
    num = math.floor(num * (10 ** places)) / (10 ** places)
    return num

def getThetaDif(theta1, theta2):
    difTheta = (theta1 - theta2) % (math.pi * 2)
    if difTheta > math.pi:
        difTheta = (math.pi * 2) - difTheta
    return difTheta

