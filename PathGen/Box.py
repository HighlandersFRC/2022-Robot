import math
import Convert

class Box:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2  = y2

    def isMouseOver(self, pygame):
        x = pygame.mouse.get_pos()[0]
        y = pygame.mouse.get_pos()[1]

        if x >= self.x1 and x <= self.x2 and y >= self.y1 and y <= self.y2:
            return True
        else:
            return False
        
        