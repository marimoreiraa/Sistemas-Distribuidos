import json
import paho.mqtt.client as mqtt

class MQTTPublisher:

    def __init__(self, broker, port, topic):
        self.client = mqtt.Client()
        self.client.connect(broker, port)
        self.topic = topic

    def publish(self, player_id, x, y, direction,color,time):

        message = {
            "player_id": player_id,
            "x": x,
            "y": y,
            "direction": direction,
            "color": color,
            "time": time
        }
        self.client.publish(self.topic, json.dumps(message))