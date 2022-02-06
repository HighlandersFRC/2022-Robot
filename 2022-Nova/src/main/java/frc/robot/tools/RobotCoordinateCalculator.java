package frc.robot.tools;

import frc.robot.subsystems.Peripherals;

public class RobotCoordinateCalculator {

    private Peripherals peripherals;

    private double fieldXCenter = 8.2296; // m
    private double fieldYCenter = 4.1148; // m
    
    public RobotCoordinateCalculator(Peripherals peripherals) {
        this.peripherals = peripherals;
    }

    public double[] getCameraAdjustedCoordinates(double[] targetCenterCoordinates) {
        double[] fieldCoordinateArray = new double[1];
        double navxAngle = Math.toRadians(peripherals.getNavxAngle());

        double angleFromTarget = (navxAngle + Math.PI/2)%(Math.PI);

        double distToTarget = targetCenterCoordinates[0];
        // double yVal = targetCenterCoordinates[1];
        double targetAngleInFrame = targetCenterCoordinates[2];

        double totalAngle = navxAngle + targetAngleInFrame;

        double targetRelYCoordinate = distToTarget * (Math.sin(totalAngle));
        double targetRelXCoordinate = distToTarget * (Math.cos(totalAngle));

        double fieldXCoordinate = fieldXCenter + targetRelXCoordinate;
        double fieldYCoordinate = fieldYCenter + targetRelYCoordinate;

        fieldCoordinateArray[0] = fieldXCoordinate;
        fieldCoordinateArray[1] = fieldYCoordinate;

        return fieldCoordinateArray;

    }

}
