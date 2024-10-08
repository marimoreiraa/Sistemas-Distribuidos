import socket
import json
import csv
import xml.etree.ElementTree as ET
import yaml
import toml


# Função para tratar as mensagens recebidas
def process_message(message, format_type):
    if format_type == "json":
        data = json.loads(message)
    elif format_type == "csv":
        reader = csv.reader([message])
        data = {
            key: value
            for key, value in zip(["Nome", "CPF", "idade", "mensagem"], next(reader))
        }
    elif format_type == "xml":
        root = ET.fromstring(message)
        data = {child.tag: child.text for child in root}
    elif format_type == "yaml":
        data = yaml.safe_load(message)
    elif format_type == "toml":
        data = toml.loads(message)
    else:
        data = {}
    return data


# Configurações do servidor
HOST = "localhost"
PORT = 12345

# Inicia o servidor
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print("Servidor aguardando conexão...")
    conn, addr = server_socket.accept()
    with conn:
        print(f"Conectado por {addr}")

        for _ in range(5):  # Receber 5 mensagens, uma de cada formato
            format_type = conn.recv(1024).decode()  # Recebe o tipo de formato
            message = conn.recv(4096).decode()  # Recebe a mensagem serializada

            # Exibe a mensagem crua recebida antes de desserializar
            print(f"\nMensagem recebida no formato {format_type}:")
            print(message)

            # Processa e exibe a mensagem desserializada
            data = process_message(message, format_type)
            print(f"\nDados processados ({format_type}):")
            print(data)
