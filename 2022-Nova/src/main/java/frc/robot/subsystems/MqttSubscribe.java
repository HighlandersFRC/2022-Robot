// package frc.robot.subsystems;

// import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
// import org.eclipse.paho.client.mqttv3.MqttCallback;
// import org.eclipse.paho.client.mqttv3.MqttClient;
// import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
// import org.eclipse.paho.client.mqttv3.MqttException;
// import org.eclipse.paho.client.mqttv3.MqttMessage;
// import org.eclipse.paho.client.mqttv3.persist.MemoryPersistence;

// public class MqttSubscribe implements MqttCallback  {

// 	/** The broker url. */
// 	private static final String brokerUrl ="tcp://10.44.99.11";

// 	/** The client id. */
// 	private static final String clientId = "clientId12";

// 	/** The topic. */
// 	private static final String topic = "/sensors/camera";

// 	public static void main(String[] args) {

// 		System.out.println("Subscriber running");
// 		new MqttSubscribe().subscribe(topic);

// 	}

// 	public void subscribe(String topic) {
// 		//	logger file name and pattern to log
// 		MemoryPersistence persistence = new MemoryPersistence();

// 		try
// 		{

// 			MqttClient sampleClient = new MqttClient(brokerUrl, clientId, persistence);
// 			MqttConnectOptions connOpts = new MqttConnectOptions();
// 			connOpts.setCleanSession(true);

// 			System.out.println("checking");
// 			System.out.println("Mqtt Connecting to broker: " + brokerUrl);

// 			sampleClient.connect(connOpts);
// 			System.out.println("Mqtt Connected");

// 			sampleClient.setCallback(this);
// 			sampleClient.subscribe(topic);

// 			System.out.println("Subscribed");
// 			System.out.println("Listening");


// 		} catch (MqttException me) {
// 			System.out.println(me);
// 		}
// 	}

// 	 //Called when the client lost the connection to the broker
// 	public void connectionLost(Throwable arg0) {
		
// 	}

// 	//Called when a outgoing publish is complete
// 	public void deliveryComplete(IMqttDeliveryToken arg0) {

// 	}

// 	public void messageArrived(String topic, MqttMessage message) throws Exception {

// 		System.out.println("| Topic:" + topic);
// 		System.out.println("| Message: " +message.toString());
// 		System.out.println("-------------------------------------------------");

// 	}

// }
