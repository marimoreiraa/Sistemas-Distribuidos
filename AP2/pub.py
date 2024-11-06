import sys
import paho.mqtt.client as paho
import time

broker = "localhost"  # Endereço do broker MQTT
port = 1883  # Porta padrão para MQTT

device_id = "dispositivo_1"  # Identificação do dispositivo (deve ser modificado em cada máquina)


# Callback chamado após publicar uma mensagem
def on_publish(client, userdata, result):
    print(f"{device_id}: Movimento publicado.")
    pass  # Não realiza nenhuma ação adicional além de exibir a mensagem


# Configuração do cliente MQTT
client = paho.Client(device_id)  # Cria o cliente com o ID do dispositivo
client.on_publish = on_publish  # Define a função de callback para publicação
client.connect(broker, port)  # Conecta ao broker MQTT

# Verifica se uma direção foi passada como argumento
if len(sys.argv) > 1:
    direction = sys.argv[1]  # Pega a direção do argumento

    # Cria a mensagem com o ID do dispositivo e a direção
    message = f"{device_id}: {direction}"
    time.sleep(0.1)  # Pausa antes de publicar

    # Publica a mensagem no tópico do jogo
    client.publish("game/move", message)

# Pausa para evitar sobrecarga de mensagens
time.sleep(0.1)

print("\nParou...")  # Indica que o processo foi encerrado
