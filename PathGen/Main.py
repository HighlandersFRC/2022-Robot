from select import select
import pygame
import File
import math
from Draw import Draw
import Point
import Transfer
import Convert
from datetime import datetime

pygame.init()

screenWidth = 1600
screenHeight = 500

selectedValue = 0
prevSelectedValue = 0
selectedPoint = None
editorString = ''
editorString2 = ''
fileName = "Path-1"
saveName = "Find Save File"

backgroundImg = pygame.image.load("Images/RapidReactField.png")
newScreenWidth = ((screenHeight / int(backgroundImg.get_height())) * backgroundImg.get_width())

fieldWidth = newScreenWidth
fieldHeight = screenHeight

backgroundImg = pygame.transform.scale(backgroundImg, (newScreenWidth, screenHeight))

font = pygame.font.SysFont("Corbel", 24)

screen = pygame.display.set_mode([screenWidth, screenHeight]) 
pygame.display.set_caption("PathGen")

draw = Draw(pygame, screen, backgroundImg, screenWidth, screenHeight, font, fieldWidth, fieldHeight, Point.getPoints())

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONUP:
            selectedPoint = Point.clicked(Convert.getFieldPos(pygame.mouse.get_pos()), fieldWidth, fieldHeight, pygame, selectedPoint, newScreenWidth, draw)
            if selectedPoint != None:
                selectedPoint = draw.clickedInfo(selectedPoint, fileName)
            command = draw.uploadButtons(fileName)
            if command == 'cleared':
                selectedPoint = None
        
        if event.type == pygame.KEYDOWN:
            if selectedPoint != None:
                if event.key in (pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_PERIOD):
                    editorString += event.unicode
                if event.key == pygame.K_BACKSPACE:
                    if len(editorString) > 0:
                        editorString = editorString.rstrip(editorString[len(editorString) - 1])
                    if len(editorString2) > 0:
                        editorString2 = editorString2.rstrip(editorString2[len(editorString2) - 1])
                else:
                    editorString2 += event.unicode
                if selectedValue == 1:
                    if editorString != '':
                        selectedPoint.angle = Convert.degreesToRadians(float(editorString))
                        selectedPoint.angle = selectedPoint.angle % (math.pi * 2)
                if selectedValue == 2:
                    if editorString != '':
                        selectedPoint.speed = float(editorString)
                if selectedValue == 3:
                    if editorString != '' and float(editorString) > 0:
                        selectedPoint.deltaTime = float(editorString)
                        draw.setTotalTime(Point.updatePointTimes())
                if selectedValue == 4:
                    if editorString != '':
                        selectedPoint.x = float(editorString)
                if selectedValue == 5:
                    if editorString != '':
                        selectedPoint.y = float(editorString)
                if selectedValue == 6:
                    fileName = editorString2.rstrip("\r")
                if selectedValue == 7:
                    saveName = editorString2.rstrip("\r")
                if selectedValue == 8 and not event.key in (pygame.K_0, pygame.K_PERIOD):
                    selectedPoint.interpolationRange = float(editorString)
            if event.key == pygame.K_RETURN:
                selectedPoint.angle = selectedPoint.angle % 360
                if selectedValue == 7:
                    fileName = draw.getFile().getSave(saveName, fieldWidth, fieldHeight)
                    selectedPoint = None
                    if fileName == None:
                        fileName = "Path-1"
                        draw.setMsg("No path found")
                    else:
                        draw.setMsg("Path opened", (15, 168, 30))
                    fileName = fileName.removesuffix(".json")
                    fileName = fileName.removeprefix("json-paths\\")
                if selectedPoint != None:
                    Point.saveSelectedPoint(selectedPoint, fieldWidth, fieldHeight)                 
                editorString = ''
                editorString2 = ''
            
    ############

    draw.drawField()
    draw.drawPoints()
    draw.drawMouseCoords(fileName)
    if selectedPoint != None:
        selectedValue = draw.drawPointInfo(selectedPoint, fileName, saveName)
        if selectedValue != prevSelectedValue:
            editorString = ''
            editorString2 = ''
        #print(selectedValue)
        prevSelectedValue = selectedValue

    ############
    pygame.display.flip()

pygame.quit()