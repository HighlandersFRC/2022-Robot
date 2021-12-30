import math
from datetime import datetime

def degreesToRadians(degrees):
    return degrees * (math.pi / 180)

def radiansToDegrees(radians):
    return radians * (180 / math.pi)

def getFieldPos(mousePos, fieldWidth, fieldHeight):
    mousePos = list(mousePos)

    mousePos[0] -= 218 * (fieldWidth / 1600)
    mousePos[1] = -1 * (mousePos[1] - (759 * (fieldHeight / 900)))

    mousePos[0] = math.floor((mousePos[0] * (1600 / fieldWidth)) * (15.98295 / 1057) * 100) / 100
    mousePos[1] = math.floor((mousePos[1] * (900 / fieldHeight)) * (15.98295 / 1057) * 100) / 100

    return mousePos

def getPixelPos(point, fieldWidth, fieldHeight):
    point = list(point)

    pixelX = (point[0] / ((1600 / fieldWidth) * (15.98295 / 1057)) ) + 218 * (fieldWidth / 1600)
    pixelY = -1 *(point[1] / ((900 / fieldHeight) * (15.98295 / 1057)) ) + 759 * (fieldHeight / 900)

    pixelPos = (pixelX, pixelY)

    return pixelPos


def getDist(x1, y1, x2, y2):
    return math.sqrt( ( (x1 - x2) * (x1 - x2) ) + ( (y1 - y2) * (y1 - y2) ) )