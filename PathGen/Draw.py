import math
from functools import cache
import Point
import Convert
from File import File
import colorsys
import hashlib

class Draw:

    def __init__(self, pygame, screen, field, screenWidth, screenHeight, font, fieldWidth, fieldHeight, points):
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
        self.colorVeloc = False
        self.colorAccel = False
        self.xOffset = 315
        self.wheelList = [[], [], []]
        self.lowerAccelBound = -9.8
        self.upperAccelBound = 9.8
        self.upperVelocBound = 5
        self.points = points
        self.wheels = []
        self.samplePeriod = 0.01
        self.file = File()

    def getFile(self):
        return self.file

    def setTotalTime(self, time):
        if time > 0.0:
            self.totalTime = time

    def setMsg(self, msg, msgColor=(255, 0, 0)):
        self.msg = msg
        self.msgColor = msgColor

    def drawField(self):
        self.pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, self.screenWidth, self.screenHeight))
        self.screen.blit(self.field, (0, 0))

        self.pygame.draw.line(self.screen, (0, 0, 0), (150, 472), (150, 425), 3)
        self.pygame.draw.line(self.screen, (0, 0, 0), (150, 472), (197, 472), 3)

        self.pygame.draw.line(self.screen, (0, 0, 0), (150, 425), (140, 435), 3)
        self.pygame.draw.line(self.screen, (0, 0, 0), (150, 425), (160, 435), 3)

        self.pygame.draw.line(self.screen, (0, 0, 0), (197, 472), (187, 482), 3)
        self.pygame.draw.line(self.screen, (0, 0, 0), (197, 472), (187, 462), 3)

        x = self.font.render('+X', True, (0, 0, 0))
        self.screen.blit(x, (160, 474))

        y = self.font.render('+Y', True, (0, 0, 0))
        self.screen.blit(y, (120, 445))

    def drawPoints(self):
        mousePosPixels = list(self.pygame.mouse.get_pos())

        if len(self.points) > 0:
            prevX = self.points[0].pixelX
            prevY = self.points[0].pixelY

        for point in self.points:
            radius = 4
            if Convert.getDist(mousePosPixels[0], mousePosPixels[1], point.pixelX, point.pixelY) < 4 or point.color == (0, 0, 255):
                radius = 6
            #self.pygame.draw.line(self.screen, (255, 0, 0), (prevX, prevY), (point.pixelX, point.pixelY), 3)
            self.drawConstAccelPath()
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

        #Color Velocity and Acceleration buttons
        color = self.font.render("Color...", True, (255, 255, 255))
        self.screen.blit(color, (1475, 100))

        if self.colorAccel:
            accelColor = (0, 255, 0)
        else:
            accelColor = (255, 0, 0)

        if self.colorVeloc:
            velocColor = (0, 255, 0)
        else:
            velocColor = (255, 0, 0)

        self.pygame.draw.rect(self.screen, accelColor, (1475, 130, 70, 50))
        self.pygame.draw.rect(self.screen, velocColor, (1475, 200, 70, 50))

        accel = self.font.render("Accel", True, (0, 0, 0))
        veloc = self.font.render("Veloc", True, (0, 0, 0))

        self.screen.blit(accel, (1483, 142))
        self.screen.blit(veloc, (1483, 212))

        #Acceleration and Velocity Key
        if self.colorAccel:
            lAccelBound = self.font.render(f"{self.lowerAccelBound} m/s^2", True, (255, 255, 255))
            uAccelBound = self.font.render(f"{self.upperAccelBound} m/s^2", True, (255, 255, 255))

            self.screen.blit(uAccelBound, (1475, 255))
            self.screen.blit(lAccelBound, (1475, 405))

            self.pygame.draw.rect(self.screen, (255, 255, 255), (1497, 280, 50, 120), width=2)

            for i in range(117):
                c = colorsys.hsv_to_rgb((117 - i) / 117, 1, 1)
                c = tuple(255 * x for x in c)
                self.pygame.draw.line(self.screen, c, (1499, 282 + i), (1545, 282 + i), 1)

        elif self.colorVeloc:
            uVelocBound = self.font.render(f"{self.upperVelocBound} m/s", True, (255, 255, 255))
            zero = self.font.render("0 m/s", True, (255, 255, 255))

            self.screen.blit(uVelocBound, (1475, 255))
            self.screen.blit(zero, (1475, 405))

            self.pygame.draw.rect(self.screen, (255, 255, 255), (1497, 280, 50, 120), width=2)

            for i in range(117):
                c = colorsys.hsv_to_rgb((117 - i) / 117, 1, 1)
                c = tuple(255 * x for x in c)
                self.pygame.draw.line(self.screen, c, (1499, 282 + i), (1545, 282 + i), 1)

        #Delete all button
        self.pygame.draw.rect(self.screen, (255, 0, 0), (975 + self.xOffset, 300, 50, 50))
        delAll1 = self.font.render("DEL", True, (0, 0, 0))
        delAll2 = self.font.render("ALL", True, (0, 0, 0))
        self.screen.blit(delAll1, (979 + self.xOffset, 303))
        self.screen.blit(delAll2, (979 + self.xOffset, 325))

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
        self.screen.blit(timeToPoint, (1005 + self.xOffset, 425))
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
        command = ''

        #Upload path
        if x >= 1050 + self.xOffset and x <= 1150 + self.xOffset and y >= 100 and y <= 150:
            bool = Point.savePath(fileName)
            self.file.connect()
            try:
                self.file.uploadFile('json-paths/' + fileName + '.json')
                self.setMsg('Uploaded Path', (15, 168, 30))
            except:
                if not bool:
                    self.setMsg('No Path to Upload')
                else:
                    self.setMsg('Upload Failed')

        #Upload all paths
        if x >= 1050 + self.xOffset and x <= 1150 + self.xOffset and y >= 200 and y <= 250:
            Point.savePath(fileName)
            self.file.connect()
            try:
                self.file.uploadAll()
                self.setMsg('Uploaded All Paths', (15, 168, 30))
            except:
                self.setMsg('Upload All Failed')

        #Download all paths
        if x >= 1050 + self.xOffset and x <= 1150 + self.xOffset and y >= 300 and y <= 350:
            self.file.connect()
            try:
                self.file.downloadAll()
                self.setMsg('Downloaded All Paths', (15, 168, 30))
            except:
                self.setMsg('Download Failed')

        #Toggle path visibility
        if x >= 975 + self.xOffset and x <= 1025 + self.xOffset and y >= 225 and y <= 275:
            self.showWheelPaths = not self.showWheelPaths

        #Delete all points
        if x >= 975 + self.xOffset and x <= 1150 + self.xOffset and y >= 300 and y <= 350:
            Point.clearPoints()
            command = 'cleared'

        #Color acceleration and velocity buttons
        if x >= 1475 and x <= 1545 and y >= 130 and y <= 180:
            self.colorAccel = not self.colorAccel
            self.colorVeloc = False
        if x >= 1475 and x <= 1545 and y >= 200 and y <= 250:
            self.colorAccel = False
            self.colorVeloc = not self.colorVeloc

        return command

    def drawConstAccelPath(self):
        time = self.points[0].time
        endTime = self.points[-1].time
        val = ''
        for p in self.points:
            val = val + str(p.x) + str(p.y) + str(p.time) + str(p.interpolationRange) + str(p.angle)
        m = hashlib.sha256(val.encode('utf-8')).hexdigest()

        while time <= endTime:
            posList = self.sampleInterpPos(time, str(m))
            pixelPosList = list(Convert.getPixelPos(x) for x in posList)

            if self.showWheelPaths:
                self.drawWheelColors(posList[1], posList[2], posList[3], posList[4], self.samplePeriod)
            self.pygame.draw.circle(self.screen, (255, 0, 0), pixelPosList[0], 1)

            time += self.samplePeriod

    def drawWheelColors(self, fL, fR, bL, bR, samplePeriod):
        flColor = (255, 0, 255)
        frColor = (255, 0, 255)
        blColor = (255, 0, 255)
        brColor = (255, 0, 255)

        fLp = Convert.getPixelPos(fL)
        fRp = Convert.getPixelPos(fR)
        bLp = Convert.getPixelPos(bL)
        bRp = Convert.getPixelPos(bR)

        self.updateWheelPoints([fL, fR, bL, bR])

        l = self.getNumWheelsPoints()

        if l >= 2 and self.colorVeloc:
            flv = (Convert.getDist(self.wheelList[0][0][0], self.wheelList[0][0][1], self.wheelList[1][0][0], self.wheelList[1][0][1]) / samplePeriod)
            frv = (Convert.getDist(self.wheelList[0][1][0], self.wheelList[0][1][1], self.wheelList[1][1][0], self.wheelList[1][1][1]) / samplePeriod)
            blv = (Convert.getDist(self.wheelList[0][2][0], self.wheelList[0][2][1], self.wheelList[1][2][0], self.wheelList[1][2][1]) / samplePeriod)
            brv = (Convert.getDist(self.wheelList[0][3][0], self.wheelList[0][3][1], self.wheelList[1][3][0], self.wheelList[1][3][1]) / samplePeriod)

            upperVelocBound = self.upperVelocBound

            if flv > upperVelocBound:
                flColor = (0, 0, 0)
            else:
                flColor = colorsys.hsv_to_rgb(flv / upperVelocBound, 1, 1)
                flColor = tuple(255 * x for x in flColor)
            
            if frv > upperVelocBound:
                frColor = (0, 0, 0)
            else:
                frColor = colorsys.hsv_to_rgb(frv / upperVelocBound, 1, 1)
                frColor = tuple(255 * x for x in frColor)

            if blv > upperVelocBound:
                blColor = (0, 0, 0)
            else:
                blColor = colorsys.hsv_to_rgb(blv / upperVelocBound, 1, 1)
                blColor = tuple(255 * x for x in blColor)

            if brv > upperVelocBound:
                brColor = (0, 0, 0)
            else:
                brColor = colorsys.hsv_to_rgb(brv / upperVelocBound, 1, 1)
                brColor = tuple(255 * x for x in brColor)

        if l == 3 and self.colorAccel:
            flv1 = (Convert.getDist(self.wheelList[0][0][0], self.wheelList[0][0][1], self.wheelList[1][0][0], self.wheelList[1][0][1]) / samplePeriod)
            frv1 = (Convert.getDist(self.wheelList[0][1][0], self.wheelList[0][1][1], self.wheelList[1][1][0], self.wheelList[1][1][1]) / samplePeriod)
            blv1 = (Convert.getDist(self.wheelList[0][2][0], self.wheelList[0][2][1], self.wheelList[1][2][0], self.wheelList[1][2][1]) / samplePeriod)
            brv1 = (Convert.getDist(self.wheelList[0][3][0], self.wheelList[0][3][1], self.wheelList[1][3][0], self.wheelList[1][3][1]) / samplePeriod)

            flv2 = (Convert.getDist(self.wheelList[1][0][0], self.wheelList[1][0][1], self.wheelList[2][0][0], self.wheelList[2][0][1]) / samplePeriod)
            frv2 = (Convert.getDist(self.wheelList[1][1][0], self.wheelList[1][1][1], self.wheelList[2][1][0], self.wheelList[2][1][1]) / samplePeriod)
            blv2 = (Convert.getDist(self.wheelList[1][2][0], self.wheelList[1][2][1], self.wheelList[2][2][0], self.wheelList[2][2][1]) / samplePeriod)
            brv2 = (Convert.getDist(self.wheelList[1][3][0], self.wheelList[1][3][1], self.wheelList[2][3][0], self.wheelList[2][3][1]) / samplePeriod)

            flA = (flv2 - flv1) / samplePeriod
            frA = (frv2 - frv1) / samplePeriod
            blA = (blv2 - blv1) / samplePeriod
            brA = (brv2 - brv1) / samplePeriod

            upperAccelBound = self.upperAccelBound
            lowerAccelBound = self.lowerAccelBound

            if flA > upperAccelBound:
                flColor = (0, 0, 0)
            elif flA < lowerAccelBound:
                flColor = (0, 0, 0)
            else:
                flColor = colorsys.hsv_to_rgb((flA + abs(lowerAccelBound)) / (upperAccelBound - lowerAccelBound), 1, 1)
                flColor = tuple(255 * x for x in flColor)

            if frA > upperAccelBound:
                frColor = (0, 0, 0)
            elif frA < lowerAccelBound:
                frColor = (0, 0, 0)
            else:
                frColor = colorsys.hsv_to_rgb((frA + abs(lowerAccelBound)) / (upperAccelBound - lowerAccelBound), 1, 1)
                frColor = tuple(255 * x for x in frColor)

            if blA > upperAccelBound:
                blColor = (0, 0, 0)
            elif blA < lowerAccelBound:
                blColor = (0, 0, 0)
            else:
                blColor = colorsys.hsv_to_rgb((blA + abs(lowerAccelBound)) / (upperAccelBound - lowerAccelBound), 1, 1)
                blColor = tuple(255 * x for x in blColor)

            if brA > upperAccelBound:
                brColor = (0, 0, 0)
            elif brA < lowerAccelBound:
                brColor = (0, 0, 0)
            else:
                brColor = colorsys.hsv_to_rgb((brA + abs(lowerAccelBound)) / (upperAccelBound - lowerAccelBound), 1, 1)
                brColor = tuple(255 * x for x in brColor)

        self.pygame.draw.circle(self.screen, flColor, fLp, 1)
        self.pygame.draw.circle(self.screen, frColor, fRp, 1)
        self.pygame.draw.circle(self.screen, blColor, bLp, 1)
        self.pygame.draw.circle(self.screen, brColor, bRp, 1)

    def getNumWheelsPoints(self):
        n = 0
        if self.wheelList[0]:
            n += 1
        if self.wheelList[1]:
            n += 1
        if self.wheelList[2]:
            n += 1
        return n

    def updateWheelPoints(self, wheels):
        self.wheelList[2] = self.wheelList[1]
        self.wheelList[1] = self.wheelList[0]
        self.wheelList[0] = wheels

    def optimizePathTimes(self):
        pass

    def updateWheelList(self, wheels, time):
        listLength = self.points[-1].time / time

    @cache
    def getWheelsAtPoint(self, center, angle):
        pi = math.pi
        distM = 0.39513
        fLAngle = ((3 * pi) / 4) + angle
        fRAngle = (pi / 4) + angle
        bLAngle = ((5 * pi) / 4) + angle
        bRAngle = ((7 * pi) / 4) + angle

        x = list(center)[0]
        y = list(center)[1]

        fL = (x + distM * math.cos(fLAngle), y + distM * math.sin(fLAngle))
        fR = (x + distM * math.cos(fRAngle), y + distM * math.sin(fRAngle))
        bL = (x + distM * math.cos(bLAngle), y + distM * math.sin(bLAngle))
        bR = (x + distM * math.cos(bRAngle), y + distM * math.sin(bRAngle))

        return [center, fL, fR, bL, bR]

    @cache
    def sampleInterpPos(self, time, hash):
        #return array format [center, fL, fR, bL, bR]
        pi = math.pi
        currentPointIndex = 0
        lowestTimeDiff = 0
        wheels = []

        timeDiffArray = []

        #If path has more than 1 point, find 2 points given time is between
        if len(self.points) > 1:
            for p in self.points:
                if p.time <= time and self.points[p.index + 1].time > time:
                    p1 = p
                    p2 = self.points[p.index + 1]

                    if p1.angle >= p2.angle:
                        op2 = ((pi * 2) - (p1.angle - p2.angle))
                        op1 = (p1.angle - p2.angle)
                    else:
                        op1 = ((pi * 2) - (p2.angle - p1.angle))
                        op2 = (p2.angle - p1.angle)

                    if op1 <= op2:
                        sine = -1
                        difWheelTheta = op1
                    else:
                        sine = 1
                        difWheelTheta = op2

                    wheelTheta = (p1.angle + ((difWheelTheta * ((time - p1.time) / (p2.time - p1.time))) * sine)) % (pi * 2)

        #Setting time diff array
        if len(self.points) > 1:
            for i in range(len(self.points)):
                timeDiffArray.append(abs(time - self.points[i].time))
                i += 1
        
        #Find time closest to current time
        for i in range(len(timeDiffArray)):
            if i == 0:
                lowestTimeDiff = timeDiffArray[0]
                currentPointIndex = 0
            else:
                if timeDiffArray[i] < lowestTimeDiff:
                    lowestTimeDiff = timeDiffArray[i]
                    currentPointIndex = i

        #If time is past last point
        if time >= self.points[-1].time:
            p = self.points[-1]
            wheels = self.getWheelsAtPoint((p.x, p.y), p.angle)
            return wheels

        #If time is before first point
        if time < self.points[0].time:
            p = self.points[0]
            wheels = self.getWheelsAtPoint((p.x, p.y), p.angle)
            return wheels

        currentPoint = self.points[currentPointIndex]

        #If current point is the last point
        if currentPointIndex + 1 >= len(self.points):
            p3 = currentPoint
            p2 = self.points[currentPointIndex - 1]
            
            vX = (p3.x - p2.x) / (p3.time - p2.time)
            vY = (p3.y - p2.y) / (p3.time - p2.time)

            x = p2.x + (vX * (time - p2.time))
            y = p2.y + (vY * (time - p2.time))

            wheels = self.getWheelsAtPoint((x, y), wheelTheta)
            return wheels

        #If current point is the first point
        if currentPointIndex == 0:
            p1 = currentPoint
            p2 = self.points[1]

            vX = (p2.x - p1.x) / (p2.time - p1.time)
            vY = (p2.y - p1.y) / (p2.time - p1.time)

            x = p1.x + (vX * (time - p1.time))
            y = p1.y + (vY * (time - p1.time))

            wheels = self.getWheelsAtPoint((x, y), wheelTheta)
            return wheels

        p1 = self.points[currentPointIndex - 1]
        p2 = currentPoint
        p3 = self.points[currentPointIndex + 1]

        interpFactor = p2.interpolationRange

        timeDif1 = p2.time - p1.time

        timeDif2 = p3.time - p2.time

        tau = min(timeDif1, timeDif2)

        t1 = p2.time - (1 - interpFactor) * tau
        t2 = p2.time + (1 - interpFactor) * tau

        timeRatio = (p2.time - p1.time) / (p3.time - p2.time)
        

        v1X = (p2.x - p1.x) / (timeDif1)
        v1Y = (p2.y - p1.y) / (timeDif1)
        v2X = (p3.x - p2.x) / (timeDif2)
        v2Y = (p3.y - p2.y) / (timeDif2)

        # print(f"v1X {v1X}")
        # print(f"v2X {v2X}")
        # print(f"v1Y {v1Y}")
        # print(f"v2Y {v2Y}")

        #If on the line segment between previous point and current point
        if time < t1:

            x = p1.x + (v1X * (time - p1.time))
            y = p1.y + (v1Y * (time - p1.time))

            wheels = self.getWheelsAtPoint((x, y), wheelTheta)
            return wheels

        #If on the line segment between current point and next point
        if time >= t2:

            x = p2.x + (v2X * (time - p2.time))
            y = p2.y + (v2Y * (time - p2.time))
            wheels = self.getWheelsAtPoint((x, y), wheelTheta)
            return wheels

        #If inside the interpolation range
        if time >= t1 and time < t2:
            interpTime = time - t1

            #Calculate accelerations
            accelX = ((v2X - v1X)) / ((t2 - t1))
            accelY = ((v2Y - v1Y)) / ((t2 - t1))

            #Determine point at t1
            t1X = (v1X * (t1 - p1.time)) + p1.x
            t1Y = (v1Y * (t1 - p1.time)) + p1.y

            x = ((accelX / 2) * (interpTime ** 2)) + (v1X * interpTime) + t1X
            y = ((accelY / 2) * (interpTime ** 2)) + (v1Y * interpTime) + t1Y

            wheels = self.getWheelsAtPoint((x, y), wheelTheta)
            return wheels
