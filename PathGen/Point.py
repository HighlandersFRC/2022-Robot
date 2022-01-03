from datetime import datetime
import math
import Convert
import json

points = []

class Point:
    def __init__(self, x, y, fieldWidth, fieldHeight, angle, speed, time, deltaTime, interpolationRange, color):
        self.x = x
        self.y = y
        self.pixelX = (x / ((1600 / fieldWidth) * (15.98295 / 1057)) ) + 218 * (fieldWidth / 1600)
        self.pixelY = -1 *(y / ((900 / fieldHeight) * (15.98295 / 1057)) ) + 759 * (fieldHeight / 900)
        self.angle = angle
        self.speed = speed
        self.time = time
        self.deltaTime = deltaTime
        self.interpolationRange = interpolationRange
        self.color = color
        self.index = len(points)

    def updatePixelPos(self, fieldWidth, fieldHeight):
        self.pixelX = (self.x / ((1600 / fieldWidth) * (15.98295 / 1057)) ) + 218 * (fieldWidth / 1600)
        self.pixelY = -1 *(self.y / ((900 / fieldHeight) * (15.98295 / 1057)) ) + 759 * (fieldHeight / 900)

    def toJSON(self):
        return self.__dict__
    
def clicked(mousePos, fieldWidth, fieldHeight, pygame, selectedPoint, imgWidth, draw):
    mousePixelPos = list(pygame.mouse.get_pos())
    mouseIsOnPoint = False
    for point in points:
        if Convert.getDist(mousePixelPos[0], mousePixelPos[1], point.pixelX, point.pixelY) < 4:
            point.color = (0, 0, 255)
            if selectedPoint != None:
                if point.index != selectedPoint.index:
                    points[selectedPoint.index].color = (255, 0, 0)
            selectedPoint = point
            mouseIsOnPoint = True
    if not mouseIsOnPoint and pygame.mouse.get_pos()[0] < imgWidth:
       if len(points) == 0:
            points.append( Point(mousePos[0], mousePos[1], fieldWidth, fieldHeight, 0.0, 0.0, 0.0, 0.0, 0.0, (255, 0, 0)))
       else:
            points.append( Point(mousePos[0], mousePos[1], fieldWidth, fieldHeight, 0.0, 0.0, 0.0, 1.0, 0.75, (255, 0, 0)))
            draw.setTotalTime(updatePointTimes())
    return selectedPoint

def saveSelectedPoint(selectedPoint, fieldWidth, fieldHeight):
    selectedPoint.angle = selectedPoint.angle % 360
    points[selectedPoint.index] = selectedPoint
    points[selectedPoint.index].updatePixelPos(fieldWidth, fieldHeight)

def getPoints():
    return points

def setPoints(newPoints):
    points.clear()
    for point in newPoints:
        points.append(point)

def deletePoint(index):
    del points[index]
    for x in range(len(points)):
        points[x].index = x
    updatePointTimes()

def savePath(fileName):
    if len(points) > 0:
        jsonPoints = []
        for point in points:
            point.color = (255, 0, 0)
            jsonPoints.append(point.toJSON())
        try:
            outfile = open(f"json-paths/{fileName}.json", "w")
            # with open(f"json-paths/{fileName}.json", "w") as outfile:
                # json.dump(jsonPoints, outfile, indent=2)
        except:
            outfile = open(f"json-paths/Path_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json", "w")
            # with open(f"json-paths/Path_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json", "w") as outfile:
        finally:
            json.dump(jsonPoints, outfile, indent=2)
            outfile.close()
        return True
    return False

def updatePointTimes():
    totalTime = 0
    for i in range(len(points)):
        totalTime += points[i].deltaTime
        points[i].time = totalTime
    return totalTime
