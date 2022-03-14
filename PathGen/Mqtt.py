import math
from paho.mqtt import client as mqtt_client

class Mqtt:
    
    def __init__(self, type):
        self.broker = '10.44.99.11'
        self.port = 1883
        self.pubTopic = "/sensors/camera"
        self.subTopic = "/pathTool"
        self.client_id = "4499-pathgen"
        self.sub_client_id = "4499-pathgen"
        self.path = []

        try:
            self.client = self.connect_mqtt()
            if type == "sub":
                self.subscribe(self.client)
                self.client.loop_start()
            else:
                self.client.loop_start()
                self.publish(self.client, "testing")
        except:
            print("Could not connect to mqtt server")

    def getPath(self):
        return self.path

    def connect_mqtt(self):
        # client_id = "44H99"
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)
        # Set Connecting Client ID
        client = mqtt_client.Client(self.client_id)
        client.username_pw_set("4499", "4499")
        client.on_connect = on_connect
        client.connect(self.broker, self.port)
        return client

    def connect_mqttSub(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker (sub)!")
            else:
                print("Failed to connect, return code %d\n", rc)
            #Set Connecting Client ID
        client = mqtt_client.Client(self.sub_client_id)
        client.username_pw_set("4499", "4499")
        client.on_connect = on_connect
        client.connect(self.broker)
        return client

    def publish(self, client, msg):
        msg_count = 0
        result = client.publish(self.pubTopic, msg)
        # result: [0, 1]
        status = result[0]
        if(status != 0):
            print("Failed to send message to Topic")
        msg_count += 1

    def subscribe(self, client):
        def on_message(client, userdata, msg):
            print("Received " + str(msg.payload.decode("utf-8")) + " from Topic " + str(self.subTopic))
            #if not msg.isDuplicate():
            #self.path.append(msg)

        # print("Listening")
        client.subscribe(self.subTopic, 2)
        client.on_message = on_message

    def on_change(self, value):
        print(value)