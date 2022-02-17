package frc.robot.tools;

import frc.robot.sensors.VisionCamera;
import frc.robot.subsystems.MqttSubscribe;
import frc.robot.subsystems.Peripherals;

public class RobotCoordinateCalculator {

    private Peripherals peripherals;

    private double fieldXCenter = 8.2296; // m
    private double fieldYCenter = 4.1148; // m

    private VisionCamera camera = new VisionCamera();
    private MqttSubscribe subscribe;
    
    public RobotCoordinateCalculator(Peripherals peripherals, MqttSubscribe subscribe) {
        this.peripherals = peripherals;
        this.subscribe = subscribe;
    }

    public double[] getCameraAdjustedCoordinates() {
        double[] fieldCoordinateArray = new double[2];
        double[] targetCenterCoordinates = camera.getVisionArray(subscribe.getLatestMessage());
        // System.out.println(targetCenterCoordinates);
        try{
            double navxAngle = Math.toRadians(peripherals.getNavxAngle());

            double angleFromTarget = (navxAngle + Math.PI/2)%(Math.PI);

            double distToTarget = (targetCenterCoordinates[0])/39.37;
            // double yVal = targetCenterCoordinates[1];
            double targetAngleInFrame = targetCenterCoordinates[1];
            // System.out.println("HELLOOOOO");

            double totalAngle = angleFromTarget + targetAngleInFrame;

            // System.out.println("Distance: " + distToTarget + " Angle: " + navxAngle);

            double targetRelYCoordinate = distToTarget * (Math.sin(totalAngle));
            double targetRelXCoordinate = distToTarget * (Math.cos(totalAngle));

            System.out.println("Angle: " + navxAngle + " X: " + targetRelXCoordinate + " Y: " + targetRelYCoordinate);

            double fieldXCoordinate = fieldXCenter - targetRelXCoordinate;
            double fieldYCoordinate = fieldYCenter - targetRelYCoordinate;

            fieldCoordinateArray[0] = fieldXCoordinate;
            fieldCoordinateArray[1] = fieldYCoordinate;

            // System.out.println("ADFASHDKflasjdf" + fieldCoordinateArray);

            return fieldCoordinateArray;
        }
        catch(Exception e) {

        }
        fieldCoordinateArray[0] = 0;
        fieldCoordinateArray[1] = 0;
        // System.out.println("NOT GETTING ANYTHING " + fieldCoordinateArray);
        return fieldCoordinateArray;
    }

}