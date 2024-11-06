import paho.mqtt.client as mqtt

broker = "localhost"  # Endereço do broker MQTT
port = 1883  # Porta padrão para MQTT
timelive = 60  # Tempo de manutenção da conexão

movimentos_recebidos = []  # Lista para armazenar os movimentos recebidos


# Callback de conexão ao servidor MQTT
def on_connect(client, userdata, flags, rc):
    print("Conectado ao servidor MQTT")
    client.subscribe(
        "game/move"
    )  # Inscreve-se no tópico "game/move" para receber movimentos


# Callback para tratar mensagens recebidas
def on_message(client, userdata, msg):
    message = msg.payload.decode()  # Decodifica a mensagem recebida

    movimentos_recebidos.append(message)  # Armazena o movimento na lista

    print(f"Movimento recebido: {message}")
    update_game(
        message
    )  # Chama a função para atualizar o jogo com o movimento recebido


# Função para processar e exibir o movimento do jogo
def update_game(message):
    device_id, direction = message.split(":")  # Separa o ID do dispositivo e a direção
    direction = direction.strip()  # Remove possíveis espaços extras na direção

    print(f"Dispositivo: {device_id}, Direção: {direction}")


# Configuração do cliente MQTT
client = mqtt.Client("subscritor")  # Cria o cliente MQTT com um identificador
client.connect(
    broker, port, timelive
)  # Conecta ao broker com o tempo limite configurado
client.on_connect = on_connect  # Define a função de callback para conexão
client.on_message = on_message  # Define a função de callback para mensagens
client.loop_forever()  # Mantém a conexão ativa para escutar mensagens continuamente
