import socket
import json
import xml.etree.ElementTree as ET
import yaml
import toml
import csv

def handle_client(conn, client):
    print(f"\nConectado com: {client}")
    while True:
        data = conn.recv(1024)
        if not data:
            break
        
        # Processar dados em cada formato
        # JSON
        try:
            data_json = json.loads(data)
            print("JSON:", data_json)
        except json.JSONDecodeError as e:
            print(f"Erro ao decodificar JSON:{e}")

        # XML
        try:
            root = ET.fromstring(data)
            print("XML:")
            for child in root:
                print(child.tag, child.text)
        except ET.ParseError as e:
            print(f"Erro ao analisar XML:{e}")

        # YAML
        try:
            data_yaml = yaml.safe_load(data)
            print("YAML:", data_yaml)
        except yaml.YAMLError as e:
            print(f"Erro ao carregar YAML: {e}")

        # TOML
        try:
            data_toml = toml.loads(data.decode('utf-8'))
            print("TOML:", data_toml)
        except (toml.TomlDecodeError, UnicodeDecodeError) as e:
            print(f"Erro ao decodificar TOML: {e}")

        # CSV
        try:
            reader = csv.reader([data.decode('utf-8')], delimiter=',')  # Ajustar o delimitador se necessário
            for row in reader:
                nome, cpf, idade, mensagem = row
                print("CSV:", nome, cpf, idade, mensagem)
        except csv.Error as e:
            print(f"Erro ao analisar CSV: {e}") 

    conn.close()
    print(f"Conexão encerrada")

host = "127.0.0.1"  # Endereço IP do servidor (localhost)
port = 5001  # Porta onde o servidor estará escutando
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
origin = (host, port)
sock.bind(origin)
sock.listen(0)
print("\nServidor iniciado e aguardando conexões...")

while True:
    conn, client = sock.accept()
    handle_client(conn,client)
