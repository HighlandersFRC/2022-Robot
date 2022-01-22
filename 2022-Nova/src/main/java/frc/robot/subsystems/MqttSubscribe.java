package frc.robot.subsystems;

import org.json.*;
import org.json.JSONObject;
import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.eclipse.paho.client.mqttv3.persist.MemoryPersistence;

public class MqttSubscribe implements MqttCallback  {

	/** The broker url. */
	private static final String brokerUrl ="tcp://10.44.99.11";

	/** The client id. */
	private static final String clientId = "clientId12";

    private double lastMessageVal = 0;

	public void subscribe(String topic) {
        Runnable task = 
        () -> {
            try
		    {
                MemoryPersistence persistence = new MemoryPersistence();

                MqttClient sampleClient = new MqttClient(brokerUrl, clientId, persistence);
                MqttConnectOptions connOpts = new MqttConnectOptions();
                connOpts.setCleanSession(true);

                System.out.println("checking");
                System.out.println("Mqtt Connecting to broker: " + brokerUrl);

                sampleClient.connect(connOpts);
                System.out.println("Mqtt Connected");

                while(true) {
                    sampleClient.setCallback(this);
                    sampleClient.subscribe(topic);

                    // System.out.println("Subscribed");
                    // System.out.println("Listening");
                }
		    } catch (MqttException me) {
                System.out.println(me);
            }
        };
        Thread thread = new Thread(task);
        thread.start();
		
	}

	 //Called when the client lost the connection to the broker
	public void connectionLost(Throwable arg0) {
		
	}

	//Called when a outgoing publish is complete
	public void deliveryComplete(IMqttDeliveryToken arg0) {

	}

    public double getLastMessageVal() {
        return lastMessageVal;
    }

	public void messageArrived(String topic, MqttMessage message) throws Exception {
		System.out.println("| Topic:" + topic);
		System.out.println("| Message: " +message.toString());
		System.out.println("-------------------------------------------------");

        lastMessageVal = new JSONObject(message.toString()).getDouble("Angle");

	}

}
