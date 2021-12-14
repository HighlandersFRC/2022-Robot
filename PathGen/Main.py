import pygame
import Draw
import Point
import Convert
import File
from datetime import datetime

pygame.init()


screenWidth = 1200
screenHeight = 500

selectedValue = 0
selectedPoint = None
editorString = ''
editorString2 = ''
fileName = "Path-1"
saveName = "Find Save File"

backgroundImg = pygame.image.load("Images/field2.png")
newScreenWidth = ((screenHeight / int(backgroundImg.get_height())) * backgroundImg.get_width())

fieldWidth = newScreenWidth
fieldHeight = screenHeight

backgroundImg = pygame.transform.scale(backgroundImg, (newScreenWidth, screenHeight))

font = pygame.font.SysFont("Corbel", 24)

screen = pygame.display.set_mode([screenWidth, screenHeight]) 
pygame.display.set_caption("PathGen")

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONUP:
            selectedPoint = Point.clicked(Convert.getFieldPos(pygame.mouse.get_pos(), fieldWidth, fieldHeight), fieldWidth, fieldHeight, pygame, selectedPoint, newScreenWidth)
            if selectedPoint != None:
                selectedPoint = Draw.clickedInfo(pygame, selectedPoint, fieldWidth, fieldHeight, fileName)
        
        if event.type == pygame.KEYDOWN:
            if selectedPoint != None:
                if event.key in (pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_PERIOD):
                    editorString += event.unicode
                editorString2 += event.unicode
                if selectedValue == 1:
                    if editorString != '':
                        selectedPoint.angle = Convert.degreesToRadians(float(editorString))
                if selectedValue == 2:
                    selectedPoint.speed = float(editorString)
                if selectedValue == 3:
                    selectedPoint.time = float(editorString)
                if selectedValue == 4:
                    selectedPoint.x = float(editorString)
                if selectedValue == 5:
                    selectedPoint.y = float(editorString)
                if selectedValue == 6:
                    fileName = editorString2.rstrip("\r")
                if selectedValue == 7:
                    saveName = editorString2.rstrip("\r")
            if event.key == pygame.K_RETURN:
                selectedPoint.angle = selectedPoint.angle % 360
                if selectedValue == 7:
                    fileName = File.getSave(saveName, fieldWidth, fieldHeight)
                    selectedPoint = None
                    if fileName == None:
                        fileName = "Path-1"
                    fileName = fileName.rstrip(".json")
                    fileName = fileName.lstrip("json-paths/\\")
                if selectedPoint != None:
                    Point.saveSelectedPoint(selectedPoint, fieldWidth, fieldHeight)                 
                editorString = ''
                editorString2 = ''
            
    ############

    Draw.drawField(backgroundImg, screen, pygame, screenWidth, screenHeight)
    Draw.drawPoints(pygame, screen, Point.getPoints())
    Draw.drawMouseCoords(pygame, screen, font, fieldWidth, fieldHeight)
    if selectedPoint != None:
        selectedValue = Draw.drawPointInfo(pygame, screen, font, selectedPoint, fileName, saveName)

    ############
    pygame.display.flip()

pygame.quit()