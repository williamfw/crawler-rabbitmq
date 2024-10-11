import os
import requests
import pika
import json
from dotenv import load_dotenv

load_dotenv()

api_url = os.getenv('URL_API', '')
host = os.getenv('RABBITMQ_HOST', '')
port = os.getenv('RABBITMQ_PORT', '')
exchange = os.getenv('EXCHANGE', '')
crawler_links_queue = os.getenv('CRAWLER_LINKS', '')
crawler_links_routing_key = os.getenv('CRAWLER_LINKS_ROUTING_KEY', '') 

ATTEMPTS_COUNT = os.getenv('ATTEMPTS_COUNT_HEADER', '')

data = None

try:
    response = requests.get(api_url)
    response.raise_for_status()
    data = response.json()
except requests.exceptions.RequestException as e:
    print(f"Erro ao consumir a API: {e}")

try:
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host, port)
    )

    channel = connection.channel()

    if data is not None:
        for item in data:    
            channel.basic_publish(
                exchange,
                crawler_links_routing_key,
                json.dumps(item), 
                pika.BasicProperties(headers = {
                    ATTEMPTS_COUNT: 0
                })
            )

        print(f"Dados enviados para a fila '{crawler_links_queue}'")

    connection.close()
except pika.exceptions.AMQPError as e:
    print(f"Erro ao enviar os dados para RabbitMQ: {e}")