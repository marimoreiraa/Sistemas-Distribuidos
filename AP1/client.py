import socket
import json
import xml.etree.ElementTree as ET
import yaml
import toml
import csv

def client_task():
    host = "127.0.0.1"  # Endereço IP do servidor (localhost)
    port = 5001        # Porta onde o servidor estará escutando
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        sock.connect((host, port))
        
        # Dados a serem enviados
        data = {
            "Nome": "Mariana",
            "CPF": 12345678,
            "idade": 23,
            "mensagem": "Esta e uma mensagem de teste"
        }
        
        # Enviar em diferentes formats
        for format in ['json', 'xml', 'yaml', 'toml', 'csv']:
            if format == 'json':
                message = json.dumps(data).encode('utf-8')
            elif format == 'xml':
                root = ET.Element("Nome")
                for key, val in data.items():
                    ET.SubElement(root, key).text = str(val)
                message = ET.tostring(root)
            elif format == 'yaml':
                message = yaml.dump(data).encode('utf-8')
            elif format == 'toml':
                message = toml.dumps(data).encode('utf-8')
            elif format == 'csv':
                csv_data = [data.values()]
                csv_string = ""
                for row in csv_data:
                    csv_string += ",".join(map(str, row)) + "\n"
                message = csv_string.encode('utf-8')

            sock.sendall(message)
            print(message)
            print(f"Mensagem no formato {format} enviada!")
    
    finally:
        sock.close()
        print(f"Conexão encerrada")

client_task()

