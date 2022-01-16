import math
import Convert

def drawWheelsOnLine(samplePeriod, theta1, theta2, difTime, v1, x1, y1, x2, y2):
        pi = math.pi
        time = 0

        totalDist = Convert.getDist(x1, y1, x2, y2)
        currentDist = 0

        accel = ((2 * totalDist) / difTime ** 2) - ((2 * v1) / difTime)

        drawTheta = math.atan2(y2 - y1, x2 - x1)

        difTheta = theta2 - theta1
        currentTheta = theta1
        if theta1 > theta2:
            difTheta = theta1 - theta2
        else:
            difTheta = theta2 - theta1
        if difTheta > pi:
            difTheta = (pi * 2) - difTheta

        while time <= difTime:
            currentDist = (v1 * time) + 0.5 * accel * (time ** 2)

            if theta1 < theta2:
                if abs(theta1 - theta2) < pi:
                    currentTheta = theta1 + (difTheta * (time / difTime))
                else:
                    currentTheta = theta1 - (difTheta * (time / difTime))
            else:
                if abs(theta1 - theta2) < pi:
                    currentTheta = theta1 - (difTheta * (time / difTime))
                else:
                    currentTheta = theta1 + (difTheta * (time / difTime))
            currentTheta = currentTheta % (pi * 2)

            point = list(Convert.getXY(currentDist, drawTheta, x1, y1))

            #self.drawWheelsAtPoint(point[0], point[1], currentTheta)
            print(currentTheta)

            time += samplePeriod

drawWheelsOnLine(0.01, 0, 3.2, 1.0, 0, 0, 0, 1, 0)