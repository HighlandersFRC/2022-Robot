import math

import pygame
import Point
import Convert
import File
import Transfer

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
            if Convert.getPixelDist(mousePosPixels[0], mousePosPixels[1], point.pixelX, point.pixelY) < 4 or point.color == (0, 0, 255):
                radius = 6
            self.pygame.draw.line(self.screen, (255, 0, 0), (prevX, prevY), (point.pixelX, point.pixelY), 3)
            prevX = point.pixelX
            prevY = point.pixelY
            self.pygame.draw.line(self.screen, (0, 255, 0), (point.pixelX - 1, point.pixelY - 1), (20 * math.cos(point.angle) + point.pixelX - 1, 20 * math.sin(point.angle) + point.pixelY - 1), 2)
            self.pygame.draw.circle(self.screen, point.color, (point.pixelX, point.pixelY), radius, 0)

    def drawMouseCoords(self, fileName):
        mouseCoords = self.font.render("#Points: " + str(len(Point.getPoints())) + "  Pos: " + str( Convert.getFieldPos(self.pygame.mouse.get_pos(), self.fieldWidth, self.fieldHeight)), True, (255, 255, 255) )
        self.screen.blit(mouseCoords, (20, 20))
        self.drawMsg()

        #Upload button
        self.pygame.draw.rect(self.screen, (255, 255, 255), (1050, 100, 100, 50))

        upload = self.font.render("UPLOAD", True, (0, 0, 0))

        self.screen.blit(upload, (1057, 115))

        #Upload all button
        self.pygame.draw.rect(self.screen, (255, 255, 255), (1050, 200, 100, 50))

        all = self.font.render("ALL", True, (0, 0, 0))

        self.screen.blit(upload, (1057, 202))
        self.screen.blit(all, (1080, 228))

    def drawMsg(self):
        text = self.font.render(str(self.msg), True, self.msgColor)
        self.screen.blit(text, (400, 50))

    def drawPointInfo(self, point, fileName, jsonName):
        pointAngleColor = (255, 255, 255)
        pointSpeedColor = (255, 255, 255)
        pointTimeColor = (255, 255, 255)
        pointXColor = (255, 255, 255)
        pointYColor = (255, 255, 255)
        pathNameColor = (255, 255, 255)
        saveNameColor = (255, 255, 255)

        infoX = 890

        x = self.pygame.mouse.get_pos()[0]
        y = self.pygame.mouse.get_pos()[1]

        sel = 0

        #Info mouse-over detection
        if x >= infoX and x <= 1000 and y >= 10 and y <= 34:
            pointAngleColor = (0, 255, 0)
            sel = 1
        
        if x >= infoX and x <= 1000 and y >= 110 and y <= 134:
            pointSpeedColor = (0, 255, 0)
            sel = 2

        if x >= infoX and x <= 1000 and y >= 150 and y <= 174:
            pointTimeColor = (0, 255, 0)
            sel = 3

        if x >= infoX and x <= 1000 and y >= 190 and y <= 214:
            pointXColor = (0, 255, 0)
            sel = 4

        if x >= infoX and x <= 1000 and y >= 270 and y <= 294:
            pointYColor = (0, 255, 0)
            sel = 5

        if x >= infoX and x <= 1000 and y >= 470 and y <= 494:
            pathNameColor = (0, 255, 0)
            sel = 6

        if x >= 1015 and x <= 1115 and y >= 10 and y <= 34:
            saveNameColor = (0, 255, 0)
            sel = 7

        #Render text
        pointAngle = self.font.render("Angle: " + str( math.floor((Convert.radiansToDegrees(point.angle)) * 10) / 10 ), True, pointAngleColor)
        pointSpeed = self.font.render("Speed: " + str( math.floor((point.speed) * 100) / 100 ), True, pointSpeedColor)
        pointTime = self.font.render("Time: " + str( math.floor((point.time) * 100) / 100 ), True, pointTimeColor)
        pointX = self.font.render("X: " + str( math.floor((point.x) * 100) / 100 ), True, pointXColor)
        pointY = self.font.render("Y: " + str( math.floor((point.y) * 100) / 100 ), True, pointYColor)
        pathName = self.font.render(fileName, True, pathNameColor)
        saveName = self.font.render(jsonName, True, saveNameColor)

        pointIndex = self.font.render("Index: " + str(point.index), True, (255, 255, 255))

        #Draw text
        self.screen.blit(pointAngle, (infoX, 10))
        self.screen.blit(pointSpeed, (infoX, 110))
        self.screen.blit(pointTime, (infoX, 150))
        self.screen.blit(pointX, (infoX, 190))
        self.screen.blit(pointY, (infoX, 270))
        self.screen.blit(pointIndex, (infoX, 350))
        self.screen.blit(pathName, (infoX, 470))
        self.screen.blit(saveName, (1015, 10))

        #Angle visual
        self.pygame.draw.circle(self.screen, (255, 255, 0), (945, 70), 35, 0)
        self.pygame.draw.line(self.screen, (255, 0, 0), (945, 70), (980, 70), 2)
        self.pygame.draw.circle(self.screen, (0, 0, 0), (945, 70), 5, 0)

        self.pygame.draw.line(self.screen, (0, 255, 0), (945, 70), (35 * math.cos(point.angle) + 945, 35 * math.sin(point.angle) + 70), 2)

        #X and Y tuning boxes
        self.pygame.draw.rect(self.screen, (255, 255, 255), (890, 215, 60, 30))
        self.pygame.draw.rect(self.screen, (255, 255, 255), (890, 295, 60, 30))

        plus = self.font.render("+", True, (0, 0, 0))
        minus = self.font.render("-", True, (0, 0, 0))

        self.screen.blit(plus, (930, 218))
        self.screen.blit(minus, (900, 218))
        self.screen.blit(plus, (930, 298))
        self.screen.blit(minus, (900, 298))

        self.pygame.draw.line(self.screen, (0, 0, 0), (920, 215), (920, 245))
        self.pygame.draw.line(self.screen, (0, 0, 0), (920, 295), (920, 325))

        #Deletion box
        self.pygame.draw.rect(self.screen, (255, 0, 0), (950, 400, 50, 50))
        delete = self.font.render("DEL", True, (0, 0, 0))
        self.screen.blit(delete, (955, 415))

        #Save to file box
        self.pygame.draw.rect(self.screen, (0, 255, 0), (900, 400, 50, 50))
        save = self.font.render("SAV", True, (0, 0, 0))
        self.screen.blit(save, (905, 415))

        self.pygame.draw.line(self.screen, (0, 0, 0), (950, 400), (950, 450))

        return sel

    def clickedInfo(self, point, fileName):
        sens = 0.05
        x = self.pygame.mouse.get_pos()[0]
        y = self.pygame.mouse.get_pos()[1]

        #X andd Y incrementation
        if x >= 890 and x <= 919 and y >= 215 and y <= 245:
            point.x -= sens
        if x >= 920 and x <= 950 and y >= 215 and y <= 245:
            point.x += sens
        if x >= 890 and x <= 919 and y >= 295 and y <= 325:
            point.y -= sens
        if x >= 920 and x <= 950 and y >= 295 and y <= 325:
            point.y += sens

        #Angle selection
        if Convert.getPixelDist(x, y, 945, 70) <= 35:
            point.angle = (math.pi / 2) - math.atan2(x - 945, y - 70)
            while point.angle < 0:
                point.angle += 2 * math.pi

        Point.saveSelectedPoint(point, self.fieldWidth, self.fieldHeight)

        #Save and delete buttons
        if x >= 900 and x < 950 and y >= 400 and y <= 450:
            Point.savePath(fileName)
            self.setMsg('Path Saved', (15, 168, 30))

        if x >= 950 and x <= 1000 and y >= 400 and y <= 450:
            Point.deletePoint(point.index)
            return None
        else:
            return point

    def uploadButtons(self, fileName):
        x = self.pygame.mouse.get_pos()[0]
        y = self.pygame.mouse.get_pos()[1]
        
        #Upload path
        if x >= 1050 and x <= 1150 and y >= 100 and y <= 150:
            Point.savePath(fileName)
            try:
                File.uploadFile('json-paths/' + fileName + '.json')
                self.setMsg('Uploaded Path', (15, 168, 30))
            except:
                self.setMsg('Upload Error')

        #Upload all paths
        if x >= 1050 and x <= 1150 and y >= 200 and y <= 250:
            Point.savePath(fileName)
            try:
                File.uploadAll()
                self.setMsg('Uploaded All Paths', (15, 168, 30))
            except:
                self.setMsg('Upload Error')
