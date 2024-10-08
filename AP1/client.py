import socket
import json
import csv
import xml.etree.ElementTree as ET
import yaml
import toml
import time


# Funções para serialização
def serialize_to_json():
    with open("AP1/msg.json", "r") as file:
        data=file.read(1024)
        file.close()
    return json.dumps(data)


def serialize_to_csv():
    with open("AP1/msg.csv", "r") as file:
        data=file.read(1024)
        file.close()
    # csv_data = ",".join([str(value) for value in data.values()])
    return data


def serialize_to_xml():
    with open("AP1/msg.xml", "r") as file:
        data=file.read(1024)
        file.close()
    # root = ET.Element("dados")
    # for key, value in data.items():
    #     child = ET.SubElement(root, key)
    #     child.text = str(value)
    # return ET.tostring(root).decode()
    return data


def serialize_to_yaml():
    with open("AP1/msg.yaml", "r") as file:
        data=file.read(1024)
        file.close()
    # return yaml.dump()
    return data


def serialize_to_toml():
    with open("AP1/msg.toml", "r") as file:
        data=file.read(1024)
        file.close()
    # return toml.dumps()
    return data


# Configurações do cliente
HOST = "localhost"
PORT = 12345

# Serializa os dados nos 5 formatos
formats = {
    "json": serialize_to_json(),
    "csv": serialize_to_csv(),
    "xml": serialize_to_xml(),
    "yaml": serialize_to_yaml(),
    "toml": serialize_to_toml(),
}

# Envia as mensagens para o servidor
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))

    for format_type, message in formats.items():
        # Imprime o tipo de formato e a mensagem antes de enviar
        print(f"\nEnviando dados no formato: {format_type}")
        print(f"Mensagem serializada ({format_type}):")
        print(message)  # Mensagem serializada que será enviada

        # Envia o tipo de formato
        client_socket.sendall(format_type.encode())
        print(f"Tipo de formato '{format_type}' enviado.")

        time.sleep(1)  # Delay para garantir que o servidor processe o formato

        # Envia a mensagem serializada
        client_socket.sendall(message.encode())
        print(f"Mensagem no formato '{format_type}' enviada.")

        time.sleep(1)  # Delay para garantir que o servidor processe a mensagem

print("Todas as mensagens foram enviadas.")
