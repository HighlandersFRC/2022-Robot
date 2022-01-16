import math

import Point
import Convert
import File

class Draw:

    def __init__(self, pygame, screen, field, screenWidth, screenHeight, font, fieldWidth, fieldHeight):
        self.pygame = pygame
        self.screen = screen
        self.field = field
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.font = font
        self.fieldWidth = fieldWidth
        self.fieldHeight = fieldHeight
        self.msg = ''
        self.msgColor = (255, 0, 0)
        self.totalTime = 0
        self.showWheelPaths = False
        self.xOffset = 315

    def setTotalTime(self, time):
        if time > 0.0:
            self.totalTime = time

    def setMsg(self, msg, msgColor=(255, 0, 0)):
        self.msg = msg
        self.msgColor = msgColor

    def drawField(self):
        self.pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, self.screenWidth, self.screenHeight))
        self.screen.blit(self.field, (0, 0))

        self.pygame.draw.line(self.screen, (0, 0, 0), (120, 422), (120, 375), 3)
        self.pygame.draw.line(self.screen, (0, 0, 0), (120, 422), (167, 422), 3)

        self.pygame.draw.line(self.screen, (0, 0, 0), (120, 375), (110, 385), 3)
        self.pygame.draw.line(self.screen, (0, 0, 0), (120, 375), (130, 385), 3)

        self.pygame.draw.line(self.screen, (0, 0, 0), (167, 422), (157, 432), 3)
        self.pygame.draw.line(self.screen, (0, 0, 0), (167, 422), (157, 412), 3)

        x = self.font.render('+X', True, (0, 0, 0))
        self.screen.blit(x, (130, 424))

        y = self.font.render('+Y', True, (0, 0, 0))
        self.screen.blit(y, (90, 395))

    def drawPoints(self, points):
        mousePosPixels = list(self.pygame.mouse.get_pos())

        if len(points) > 0:
            prevX = points[0].pixelX
            prevY = points[0].pixelY

        for point in points:
            radius = 4
            if Convert.getDist(mousePosPixels[0], mousePosPixels[1], point.pixelX, point.pixelY) < 4 or point.color == (0, 0, 255):
                radius = 6
            #self.pygame.draw.line(self.screen, (255, 0, 0), (prevX, prevY), (point.pixelX, point.pixelY), 3)
            self.drawConstAccelPath(points, 0.01)
            prevX = point.pixelX
            prevY = point.pixelY
            self.pygame.draw.line(self.screen, (0, 255, 0), (point.pixelX - 1, point.pixelY - 1), (20 * math.cos((math.pi * 2) - point.angle) + point.pixelX - 1, 20 * math.sin((math.pi * 2) - point.angle) + point.pixelY - 1), 2)
            self.pygame.draw.circle(self.screen, point.color, (point.pixelX, point.pixelY), radius, 0)

    def drawMouseCoords(self, fileName):
        pointNum = self.font.render("#Points: " + str(len(Point.getPoints())), True, (0, 0, 0))
        mouseCoords1 = self.font.render("Pos (m):", True, (0, 0, 0))
        mouseCoords2 = self.font.render(str(Convert.round(Convert.getFieldPos(self.pygame.mouse.get_pos())[0], 2)) + " X", True, (0, 0, 0))
        mouseCoords3 = self.font.render(str(Convert.round(Convert.getFieldPos(self.pygame.mouse.get_pos())[1], 2)) + " Y", True, (0, 0, 0))
        mouseCoords4 = self.font.render("PixelPos: ", True, (0, 0, 0))
        mouseCoords5 = self.font.render(str(list(self.pygame.mouse.get_pos())[0]) + " X", True, (0, 0, 0))
        mouseCoords6 = self.font.render(str(list(self.pygame.mouse.get_pos())[1]) + " Y", True, (0, 0, 0))
        self.screen.blit(mouseCoords1, (5, 50))
        self.screen.blit(mouseCoords2, (5, 70))
        self.screen.blit(mouseCoords3, (5, 90))
        self.screen.blit(mouseCoords4, (5, 120))
        self.screen.blit(mouseCoords5, (5, 140))
        self.screen.blit(mouseCoords6, (5, 160))
        self.screen.blit(pointNum, (5, 20))
        self.drawMsg()

        #Upload button
        self.pygame.draw.rect(self.screen, (255, 255, 255), (1050 + self.xOffset, 100, 100, 50))

        upload = self.font.render("UPLOAD", True, (0, 0, 0))

        self.screen.blit(upload, (1057 + self.xOffset, 115))

        #Upload all button
        self.pygame.draw.rect(self.screen, (255, 255, 255), (1050 + self.xOffset, 200, 100, 50))

        all = self.font.render("ALL", True, (0, 0, 0))

        self.screen.blit(upload, (1057 + self.xOffset, 202))
        self.screen.blit(all, (1080 + self.xOffset, 228))

        #Download all button
        self.pygame.draw.rect(self.screen, (255, 255, 255), (1050 + self.xOffset, 300, 100, 50))

        download = self.font.render("DOWNLD", True, (0, 0, 0))

        self.screen.blit(download, (1051 + self.xOffset, 302))
        self.screen.blit(all, (1080 + self.xOffset, 328))

        #Toggle path button
        if self.showWheelPaths:
            wheelColor = (0, 255, 0)
        else:
            wheelColor = (255, 0, 0)
        self.pygame.draw.rect(self.screen, wheelColor, (975 + self.xOffset, 225, 50, 50))
        wheelLabel1 = self.font.render("Whl", True, (0, 0, 0))
        wheelLabel2 = self.font.render("Path", True, (0, 0, 0))
        self.screen.blit(wheelLabel1, (980 + self.xOffset, 227))
        self.screen.blit(wheelLabel2, (978 + self.xOffset, 250))

    def drawMsg(self):
        text = self.font.render(str(self.msg), True, self.msgColor)
        self.screen.blit(text, (1350, 50))

    def drawPointInfo(self, point, fileName, jsonName):
        pointAngleColor = (255, 255, 255)
        pointSpeedColor = (255, 255, 255)
        pointTimeColor = (255, 255, 255)
        pointXColor = (255, 255, 255)
        pointYColor = (255, 255, 255)
        pathNameColor = (255, 255, 255)
        saveNameColor = (255, 255, 255)
        interpNameColor = (255, 255, 255)

        infoX = 890

        x = self.pygame.mouse.get_pos()[0]
        y = self.pygame.mouse.get_pos()[1]

        sel = 0

        #Info mouse-over detection
        if x >= infoX + self.xOffset and x <= 1000 + self.xOffset and y >= 10 and y <= 34:
            pointAngleColor = (0, 255, 0)
            sel = 1
        
        if x >= infoX + self.xOffset and x <= 1000 + self.xOffset and y >= 110 and y <= 134:
            pointSpeedColor = (0, 255, 0)
            sel = 2

        if x >= infoX + self.xOffset and x <= 1000 + self.xOffset and y >= 150 and y <= 174:
            pointTimeColor = (0, 255, 0)
            sel = 3

        if x >= infoX + self.xOffset and x <= 1000 + self.xOffset and y >= 190 and y <= 214:
            pointXColor = (0, 255, 0)
            sel = 4

        if x >= infoX + self.xOffset and x <= 1000 + self.xOffset and y >= 270 and y <= 294:
            pointYColor = (0, 255, 0)
            sel = 5

        if x >= infoX + self.xOffset and x <= 1000 + self.xOffset and y >= 470 and y <= 494:
            pathNameColor = (0, 255, 0)
            sel = 6

        if x >= 1015 + self.xOffset and x <= 1115 + self.xOffset and y >= 10 and y <= 34:
            saveNameColor = (0, 255, 0)
            sel = 7

        if x >= 1015 + self.xOffset and x <= 1115 + self.xOffset and y >= 450 and y <= 474:
            interpNameColor = (0, 255, 0)
            sel = 8

        #Render text
        pointAngle = self.font.render("Angle: " + str( math.floor((Convert.radiansToDegrees(point.angle)) * 10) / 10 ), True, pointAngleColor)
        pointSpeed = self.font.render("Speed: " + str( math.floor((point.speed) * 100) / 100 ), True, pointSpeedColor)
        pointTime = self.font.render("Time from prev: " + str( math.floor((point.deltaTime) * 100) / 100 ), True, pointTimeColor)
        pointX = self.font.render("X: " + str( math.floor((point.x) * 100) / 100 ), True, pointXColor)
        pointY = self.font.render("Y: " + str( math.floor((point.y) * 100) / 100 ), True, pointYColor)
        pathName = self.font.render(fileName, True, pathNameColor)
        saveName = self.font.render(jsonName, True, saveNameColor)

        pointIndex = self.font.render("Index: " + str(point.index), True, (255, 255, 255))
        pathTime = self.font.render("Path Time: " + str(self.totalTime), True, (255, 255, 255))
        timeToPoint = self.font.render("Time to point: " + str(point.time), True, (255, 255, 255))
        interpRange = self.font.render("Interp: " + str(point.interpolationRange), True, interpNameColor)

        #Draw text
        self.screen.blit(pointAngle, (infoX + self.xOffset, 10))
        self.screen.blit(pointSpeed, (infoX + self.xOffset, 110))
        self.screen.blit(pointTime, (infoX + self.xOffset, 150))
        self.screen.blit(pointX, (infoX + self.xOffset, 190))
        self.screen.blit(pointY, (infoX + self.xOffset, 270))
        self.screen.blit(pointIndex, (infoX + self.xOffset, 350))
        self.screen.blit(pathName, (infoX + self.xOffset, 470))
        self.screen.blit(saveName, (1015 + self.xOffset, 10))
        self.screen.blit(pathTime, (1015 + self.xOffset, 370))
        self.screen.blit(timeToPoint, (1015 + self.xOffset, 400))
        self.screen.blit(interpRange, (1015 + self.xOffset, 450))

        #Angle visual
        self.pygame.draw.circle(self.screen, (255, 255, 0), (945 + self.xOffset, 70), 35, 0)
        self.pygame.draw.line(self.screen, (255, 0, 0), (945 + self.xOffset, 70), (980 + self.xOffset, 70), 2)
        self.pygame.draw.circle(self.screen, (0, 0, 0), (945 + self.xOffset, 70), 5, 0)

        self.pygame.draw.line(self.screen, (0, 255, 0), (945 + self.xOffset, 70), (35 * math.cos((math.pi * 2) - point.angle) + 945 + self.xOffset, 35 * math.sin((math.pi * 2) - point.angle) + 70), 2)

        #X and Y tuning boxes
        self.pygame.draw.rect(self.screen, (255, 255, 255), (890 + self.xOffset, 215, 60, 30))
        self.pygame.draw.rect(self.screen, (255, 255, 255), (890 + self.xOffset, 295, 60, 30))

        plus = self.font.render("+", True, (0, 0, 0))
        minus = self.font.render("-", True, (0, 0, 0))

        self.screen.blit(plus, (930 + self.xOffset, 218))
        self.screen.blit(minus, (900 + self.xOffset, 218))
        self.screen.blit(plus, (930 + self.xOffset, 298))
        self.screen.blit(minus, (900 + self.xOffset, 298))

        self.pygame.draw.line(self.screen, (0, 0, 0), (920 + self.xOffset, 215), (920 + self.xOffset, 245))
        self.pygame.draw.line(self.screen, (0, 0, 0), (920 + self.xOffset, 295), (920 + self.xOffset, 325))

        #Deletion box
        self.pygame.draw.rect(self.screen, (255, 0, 0), (950 + self.xOffset, 400, 50, 50))
        delete = self.font.render("DEL", True, (0, 0, 0))
        self.screen.blit(delete, (955 + self.xOffset, 415))

        #Save to file box
        self.pygame.draw.rect(self.screen, (0, 255, 0), (900 + self.xOffset, 400, 50, 50))
        save = self.font.render("SAV", True, (0, 0, 0))
        self.screen.blit(save, (905 + self.xOffset, 415))

        self.pygame.draw.line(self.screen, (0, 0, 0), (950 + self.xOffset, 400), (950 + self.xOffset, 450))

        return sel

    def clickedInfo(self, point, fileName):
        sens = 0.05
        x = self.pygame.mouse.get_pos()[0]
        y = self.pygame.mouse.get_pos()[1]

        #X andd Y incrementation
        if x >= 890 + self.xOffset and x <= 919 + self.xOffset and y >= 215 and y <= 245:
            point.x -= sens
        if x >= 920 + self.xOffset and x <= 950 + self.xOffset and y >= 215 and y <= 245:
            point.x += sens
        if x >= 890 + self.xOffset and x <= 919 + self.xOffset and y >= 295 and y <= 325:
            point.y -= sens
        if x >= 920 + self.xOffset and x <= 950 + self.xOffset and y >= 295 and y <= 325:
            point.y += sens

        #Angle selection
        if Convert.getDist(x, y, 945 + self.xOffset, 70) <= 35:
            point.angle = math.atan2(y - 70, x - (945 + self.xOffset))
            while point.angle < 0:
                point.angle += 2 * math.pi
            point.angle = (math.pi * 2) - point.angle
            

        Point.saveSelectedPoint(point, self.fieldWidth, self.fieldHeight)

        #Save and delete buttons
        if x >= 900 + self.xOffset and x < 950 + self.xOffset and y >= 400 and y <= 450:
            Point.savePath(fileName)
            self.setMsg('Path Saved', (15, 168, 30))

        if x >= 950 + self.xOffset and x <= 1000 + self.xOffset and y >= 400 and y <= 450:
            Point.deletePoint(point.index)
            return None
        else:
            return point

    def uploadButtons(self, fileName):
        x = self.pygame.mouse.get_pos()[0]
        y = self.pygame.mouse.get_pos()[1]

        #Upload path
        if x >= 1050 + self.xOffset and x <= 1150 + self.xOffset and y >= 100 and y <= 150:
            bool = Point.savePath(fileName)
            try:
                File.uploadFile('json-paths/' + fileName + '.json')
                self.setMsg('Uploaded Path', (15, 168, 30))
            except:
                if not bool:
                    self.setMsg('No Path to Upload')
                else:
                    self.setMsg('Upload Failed')

        #Upload all paths
        if x >= 1050 + self.xOffset and x <= 1150 + self.xOffset and y >= 200 and y <= 250:
            Point.savePath(fileName)
            try:
                File.uploadAll()
                self.setMsg('Uploaded All Paths', (15, 168, 30))
            except:
                self.setMsg('Upload All Failed')

        #Download all paths
        if x >= 1050 + self.xOffset and x <= 1150 + self.xOffset and y >= 300 and y <= 350:
            try:
                File.downloadAll()
                self.setMsg('Downloaded All Paths', (15, 168, 30))
            except:
                self.setMsg('Download Failed')

        #Toggle path visibility
        if x >= 975 + self.xOffset and x <= 1025 + self.xOffset and y >= 225 and y <= 275:
            self.showWheelPaths = not self.showWheelPaths

    def drawConstAccelPath(self, points, samplePeriod):
        pi = math.pi
        prevInterpPoint2Meters = []
        prevT2Theta = 0
        prevT2 = 0
        prevV2 = 0
        for p in points:
            if p.index != 0 and p.index != len(points) - 1:
                p1 = points[p.index - 1]
                p2 = points[p.index]
                p3 = points[p.index + 1]

                interpFraction = p2.interpolationRange

                if interpFraction == 1:
                    interpFraction = 0.99

                t1 = p1.time + (p2.time - p1.time) * interpFraction
                t2 = p2.time + (p3.time - p2.time) * (1 - interpFraction)

                theta1 = math.atan2((p1.y - p2.y), (p1.x - p2.x))
                theta2 = math.atan2((p3.y - p2.y), (p3.x - p2.x))

                interpPoint1 = (p2.x + ((1 - interpFraction) * (Convert.getDist(p1.x, p1.y, p2.x, p2.y)) * math.cos(theta1)), p2.y + ((1 - interpFraction) * Convert.getDist(p2.x, p2.y, p1.x, p1.y)) * math.sin(theta1))
                interpPoint2 = (p2.x + ((1 - interpFraction) * (Convert.getDist(p3.x, p3.y, p2.x, p2.y)) * math.cos(theta2)), p2.y + ((1 - interpFraction) * Convert.getDist(p2.x, p2.y, p3.x, p3.y)) * math.sin(theta2))

                interpPoint1 = Convert.getPixelPos(interpPoint1)
                interpPoint2 = Convert.getPixelPos(interpPoint2)

                self.pygame.draw.line(self.screen, (255, 0, 0), ((p1.pixelX + p2.pixelX) / 2, (p1.pixelY + p2.pixelY) / 2), interpPoint1, 2)
                self.pygame.draw.line(self.screen, (255, 0, 0), ((p3.pixelX + p2.pixelX) / 2, (p3.pixelY + p2.pixelY) / 2), interpPoint2, 2)

                #self.pygame.draw.line(self.screen, (0, 255, 0), interpPoint1, interpPoint2, 2)

                interpPoint1Meters = Convert.getFieldPos(interpPoint1)
                interpPoint2Meters = Convert.getFieldPos(interpPoint2)
                interpDistMeters = Convert.getDist(interpPoint1Meters[0], interpPoint1Meters[1], interpPoint2Meters[0], interpPoint2Meters[1])

                targetTheta = pi + math.atan2((interpPoint1Meters[1] - interpPoint2Meters[1]), (interpPoint1Meters[0] - interpPoint2Meters[0]))
                targetTheta = targetTheta % (pi * 2)

                v1 = Convert.getDist(p1.x, p1.y, interpPoint1Meters[0], interpPoint1Meters[1]) / (t1 - p1.time)
                v2 = Convert.getDist(p3.x, p3.y, interpPoint2Meters[0], interpPoint2Meters[1]) / (p3.time - t2)

                if p1.angle >= p2.angle:
                    op2 = ((pi * 2) - (p1.angle - p2.angle))
                    op1 = (p1.angle - p2.angle)
                else:
                    op1 = ((pi * 2) - (p2.angle - p1.angle))
                    op2 = (p2.angle - p1.angle)

                if p2.angle >= p3.angle:
                    op3 = ((pi * 2) - (p2.angle - p3.angle))
                    op4 = (p2.angle - p3.angle)
                else:
                    op3 = ((pi * 2) - (p3.angle - p2.angle))
                    op4 = (p3.angle - p2.angle)

                if op1 <= op2:
                    sine1 = -1
                    difWheelTheta1 = op1
                else:
                    sine1 = 1
                    difWheelTheta1 = op2

                if op3 <= op4:
                    sine2 = 1
                    difWheelTheta2 = op3
                else:
                    sine2 = -1
                    difWheelTheta2 = op4

                t1Theta = (p1.angle + ((difWheelTheta1 * interpFraction) * sine1)) % (pi * 2)
                t2Theta = (p2.angle + ((difWheelTheta2 * (1 - interpFraction)) * sine2)) % (pi * 2)

                # print('1: ' + str(difWheelTheta1))
                # print('2: ' + str(difWheelTheta2))

                time = t1
                difTime = t2 - t1
                difVel = v2 - v1
                neededAccel = difVel / difTime
                endDist = (neededAccel * difTime + v1) * (difTime)
                theta1 += pi
                theta1 = theta1 % (pi * 2)

                difTheta = abs(theta1 - targetTheta)
                if difTheta > pi:
                    difTheta = (pi * 2) - difTheta

                while time <= t2 and time >= t1:
                    currentDist = ((neededAccel * (time - t1) + v1) * (time - t1)) * (interpDistMeters / endDist)

                    if time <= p2.time:
                        wheelTheta = (p1.angle + ((difWheelTheta1 * ((time - p1.time) / (p2.deltaTime))) * sine1)) % (pi * 2)
                    else:
                        wheelTheta = (p2.angle + ((difWheelTheta2 * ((time - p2.time) / (p3.deltaTime))) * sine2)) % (pi * 2)

                    if theta1 < targetTheta:
                        if abs(theta1 - targetTheta) < pi:
                            currentTheta = theta1 + (difTheta * ((time - t1) / difTime))
                        else:
                            currentTheta = theta1 - (difTheta * ((time - t1) / difTime))
                    else:
                        if abs(theta1 - targetTheta) < pi:
                            currentTheta = theta1 - (difTheta * ((time - t1) / difTime))
                        else:
                            currentTheta = theta1 + (difTheta * ((time - t1) / difTime))
                    currentTheta = currentTheta % (pi * 2)

                    x = interpPoint1Meters[0] + currentDist * math.cos(currentTheta)
                    y = interpPoint1Meters[1] + currentDist * math.sin(currentTheta)
                    point = Convert.getPixelPos((x, y))
                    
                    self.pygame.draw.circle(self.screen, (0, 255, 0), point, 1)
                    if self.showWheelPaths:
                        self.drawWheelsAtPoint(x, y, wheelTheta)

                    # print('wheelTheta: ' + str(wheelTheta))

                    time += samplePeriod

                # print('angle1: ' + str(p1.angle))
                # print('t1Theta: ' + str(t1Theta))
                # print('angle2: ' + str(p2.angle))
                # print('t2Theta: ' + str(t2Theta))
                # print('angle3: ' + str(p3.angle))
                
                
                if p1.index >= 1:

                    if prevT2Theta >= t1Theta:
                        op5 = ((pi * 2) - (prevT2Theta - t1Theta))
                        op6 = (prevT2Theta - t1Theta)
                    else:
                        op6 = ((pi * 2) - (t1Theta - prevT2Theta))
                        op5 = (t1Theta - prevT2Theta)

                    if op5 <= op6:
                        sine3 = 1
                    else:
                        sine3 = -1
                        

                    if self.showWheelPaths:
                        self.drawWheelsOnLine(samplePeriod, prevT2Theta, t1Theta, (t1 - prevT2), prevV2, prevInterpPoint2Meters[0], prevInterpPoint2Meters[1], interpPoint1Meters[0], interpPoint1Meters[1], sine3)

                if p1.index == 0:

                    if self.showWheelPaths:
                        self.drawWheelsOnLine(samplePeriod, p1.angle, t1Theta, (t1 - p1.time), 0, p1.x, p1.y, interpPoint1Meters[0], interpPoint1Meters[1], sine1)

                    self.pygame.draw.line(self.screen, (255, 0, 0), (points[0].pixelX, points[0].pixelY), ((p1.pixelX + p2.pixelX) / 2, (p1.pixelY + p2.pixelY) / 2), 2)
                    
                    
                if p3.index == len(points) - 1:

                    if self.showWheelPaths:
                       self.drawWheelsOnLine(samplePeriod, t2Theta, p3.angle, p3.deltaTime - (t2 - p2.time), v2, interpPoint2Meters[0], interpPoint2Meters[1], p3.x, p3.y, sine2)

                    self.pygame.draw.line(self.screen, (255, 0, 0), (points[-1].pixelX, points[-1].pixelY), ((p3.pixelX + p2.pixelX) / 2, (p3.pixelY + p2.pixelY) / 2), 2)

                prevInterpPoint2Meters = interpPoint2Meters
                prevT2Theta = t2Theta
                prevT2 = t2
                prevV2 = v2

                #print('t1Theta: ' + str(t1Theta))
                #print('t2Theta: ' + str(t2Theta))
            
            elif len(points) == 2:
                p1 = points[0]
                p2 = points[1]

                if self.showWheelPaths:
                    self.drawWheelsOnLine(samplePeriod, p1.angle, p2.angle, p2.deltaTime, 0, p1.x, p1.y, p2.x, p2.y, 1)

                self.pygame.draw.line(self.screen, (255, 0, 0), (points[0].pixelX, points[0].pixelY), (points[1].pixelX, points[1].pixelY), 2)

    def drawWheelsAtPoint(self, metersX, metersY, angle):
        pi = math.pi
        distM = 0.39513
        #distM = 1
        fLAngle = ((3 * pi) / 4) + angle
        fRAngle = (pi / 4) + angle
        bLAngle = ((5 * pi) / 4) + angle
        bRAngle = ((7 * pi) / 4) + angle

        fL = Convert.getPixelPos([metersX + distM * math.cos(fLAngle), metersY + distM * math.sin(fLAngle)])
        fR = Convert.getPixelPos([metersX + distM * math.cos(fRAngle), metersY + distM * math.sin(fRAngle)])
        bL = Convert.getPixelPos([metersX + distM * math.cos(bLAngle), metersY + distM * math.sin(bLAngle)])
        bR = Convert.getPixelPos([metersX + distM * math.cos(bRAngle), metersY + distM * math.sin(bRAngle)])

        self.pygame.draw.circle(self.screen, (255, 0, 255), fL, 1)
        self.pygame.draw.circle(self.screen, (255, 0, 255), fR, 1)
        self.pygame.draw.circle(self.screen, (255, 0, 255), bL, 1)
        self.pygame.draw.circle(self.screen, (255, 0, 255), bR, 1)

    def drawWheelsOnLine(self, samplePeriod, theta1, theta2, difTime, v1, x1, y1, x2, y2, sine):
        pi = math.pi
        time = 0

        totalDist = Convert.getDist(x1, y1, x2, y2)
        currentDist = 0

        accel = ((2 * totalDist) / difTime ** 2) - ((2 * v1) / difTime)

        drawTheta = math.atan2(y2 - y1, x2 - x1)

        difTheta = Convert.getThetaDif(theta1, theta2)

        while time <= difTime:
            currentDist = (v1 * time) + 0.5 * accel * (time ** 2)

            currentTheta = (theta1 + ((difTheta * ((time) / (difTime))) * sine)) % (pi * 2)

            point = list(Convert.getXY(currentDist, drawTheta, x1, y1))

            self.drawWheelsAtPoint(point[0], point[1], currentTheta)

            time += samplePeriod