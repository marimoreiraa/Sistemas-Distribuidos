import paho.mqtt.client as mqtt
import json
import game 

class MQTTSubscriber:
    def __init__(self, broker, port, topic, player_id):
        self.client = mqtt.Client()
        self.broker = broker
        self.port = port
        self.topic = topic
        self.player_id = player_id  # Armazena o ID do jogador local
        # Callback para quando uma mensagem é recebida
        self.client.on_message = self.on_message
        # Conectar ao broker
        self.client.connect(broker, port)
        # Subscriver ao tópico
        self.client.subscribe(topic)

    def on_message(self, client, userdata, msg):
        message = json.loads(msg.payload.decode())
        if message["player_id"] != self.player_id:
            print(f"Movimento recebido: {message}")
            game.update_players(message)

    def start(self):
        self.client.loop_forever()  # Manter o cliente em execução indefinidamente