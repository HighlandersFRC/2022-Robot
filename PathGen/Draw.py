import math
import Point
import Convert
import File

def drawField(field, screen, pygame, screenWidth, screenHeight):
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, screenWidth, screenHeight))
    screen.blit(field, (0, 0))

def drawPoints(pygame, screen, points):
    mousePosPixels = list(pygame.mouse.get_pos())

    if len(points) > 0:
        prevX = points[0].pixelX
        prevY = points[0].pixelY

    for point in points:
        radius = 4
        if Convert.getPixelDist(mousePosPixels[0], mousePosPixels[1], point.pixelX, point.pixelY) < 4 or point.color == (0, 0, 255):
            radius = 6
        pygame.draw.line(screen, (255, 0, 0), (prevX, prevY), (point.pixelX, point.pixelY), 3)
        prevX = point.pixelX
        prevY = point.pixelY
        pygame.draw.line(screen, (0, 255, 0), (point.pixelX - 1, point.pixelY - 1), (20 * math.cos(point.angle) + point.pixelX - 1, 20 * math.sin(point.angle) + point.pixelY - 1), 2)
        pygame.draw.circle(screen, point.color, (point.pixelX, point.pixelY), radius, 0)

def drawMouseCoords(pygame, screen, font, fieldWidth, fieldHeight):
    mouseCoords = font.render("#Points: " + str(len(Point.getPoints())) + "  Pos: " + str( Convert.getFieldPos(pygame.mouse.get_pos(), fieldWidth, fieldHeight)), True, (255, 255, 255) )
    screen.blit(mouseCoords, (20, 20))

def drawPointInfo(pygame, screen, font, point, fileName, jsonName):
    pointAngleColor = (255, 255, 255)
    pointSpeedColor = (255, 255, 255)
    pointTimeColor = (255, 255, 255)
    pointXColor = (255, 255, 255)
    pointYColor = (255, 255, 255)
    pathNameColor = (255, 255, 255)
    saveNameColor = (255, 255, 255)

    infoX = 890

    x = pygame.mouse.get_pos()[0]
    y = pygame.mouse.get_pos()[1]

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
    pointAngle = font.render("Angle: " + str( math.floor((Convert.radiansToDegrees(point.angle)) * 10) / 10 ), True, pointAngleColor)
    pointSpeed = font.render("Speed: " + str( math.floor((point.speed) * 100) / 100 ), True, pointSpeedColor)
    pointTime = font.render("Time: " + str( math.floor((point.time) * 100) / 100 ), True, pointTimeColor)
    pointX = font.render("X: " + str( math.floor((point.x) * 100) / 100 ), True, pointXColor)
    pointY = font.render("Y: " + str( math.floor((point.y) * 100) / 100 ), True, pointYColor)
    pathName = font.render(fileName, True, pathNameColor)
    saveName = font.render(jsonName, True, saveNameColor)

    pointIndex = font.render("Index: " + str(point.index), True, (255, 255, 255))

    #Draw text
    screen.blit(pointAngle, (infoX, 10))
    screen.blit(pointSpeed, (infoX, 110))
    screen.blit(pointTime, (infoX, 150))
    screen.blit(pointX, (infoX, 190))
    screen.blit(pointY, (infoX, 270))
    screen.blit(pointIndex, (infoX, 350))
    screen.blit(pathName, (infoX, 470))
    screen.blit(saveName, (1015, 10))

    #Angle visual
    pygame.draw.circle(screen, (255, 255, 0), (945, 70), 35, 0)
    pygame.draw.line(screen, (255, 0, 0), (945, 70), (980, 70), 2)
    pygame.draw.circle(screen, (0, 0, 0), (945, 70), 5, 0)

    pygame.draw.line(screen, (0, 255, 0), (945, 70), (35 * math.cos(point.angle) + 945, 35 * math.sin(point.angle) + 70), 2)

    #Upload button
    pygame.draw.rect(screen, (255, 255, 255), (1050, 100, 100, 50))

    upload = font.render("UPLOAD", True, (0, 0, 0))

    screen.blit(upload, (1057, 115))

    #Upload all button
    pygame.draw.rect(screen, (255, 255, 255), (1050, 200, 100, 50))

    all = font.render("ALL", True, (0, 0, 0))

    screen.blit(upload, (1057, 202))
    screen.blit(all, (1080, 228))

    #X and Y tuning boxes
    pygame.draw.rect(screen, (255, 255, 255), (890, 215, 60, 30))
    pygame.draw.rect(screen, (255, 255, 255), (890, 295, 60, 30))

    plus = font.render("+", True, (0, 0, 0))
    minus = font.render("-", True, (0, 0, 0))

    screen.blit(plus, (930, 218))
    screen.blit(minus, (900, 218))
    screen.blit(plus, (930, 298))
    screen.blit(minus, (900, 298))

    pygame.draw.line(screen, (0, 0, 0), (920, 215), (920, 245))
    pygame.draw.line(screen, (0, 0, 0), (920, 295), (920, 325))

    #Deletion box
    pygame.draw.rect(screen, (255, 0, 0), (950, 400, 50, 50))
    delete = font.render("DEL", True, (0, 0, 0))
    screen.blit(delete, (955, 415))

    #Save to file box
    pygame.draw.rect(screen, (0, 255, 0), (900, 400, 50, 50))
    save = font.render("SAV", True, (0, 0, 0))
    screen.blit(save, (905, 415))

    pygame.draw.line(screen, (0, 0, 0), (950, 400), (950, 450))

    return sel

def clickedInfo(pygame, point, fieldWidth, fieldHeight, fileName):
    sens = 0.05
    x = pygame.mouse.get_pos()[0]
    y = pygame.mouse.get_pos()[1]

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

    Point.saveSelectedPoint(point, fieldWidth, fieldHeight)

    #Upload path
    if x >= 1050 and x <= 1150 and y >= 100 and y <= 150:
        Point.savePath(fileName)
        File.uploadFile('json-paths/' + fileName + '.json')

    #Upload all paths
    if x >= 1050 and x <= 1150 and y >= 200 and y <= 250:
        Point.savePath(fileName)
        File.uploadAll()

    #Save and delete buttons
    if x >= 900 and x < 950 and y >= 400 and y <= 450:
        Point.savePath(fileName)

    if x >= 950 and x <= 1000 and y >= 400 and y <= 450:
        Point.deletePoint(point.index)
        return None
    else:
        return point
