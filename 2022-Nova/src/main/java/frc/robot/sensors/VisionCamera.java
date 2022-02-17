package frc.robot.sensors;

import org.json.JSONObject;

public class VisionCamera {
    
    public VisionCamera() {

    }

    public double[] getVisionArray(String message) {
        double[] visionArray = new double[2];

        try {
            JSONObject jsonString = new JSONObject(message);

            visionArray[0] = jsonString.getDouble("Distance");
            visionArray[1] = jsonString.getDouble("Angle");

            // System.out.println(visionArray[0]);

            return visionArray;
        }
        catch(Exception e) {
            // System.out.println("Didn't receive message");
        }

        visionArray[0] = -1;
        visionArray[1] = -100;
        return visionArray;
        
    }

}