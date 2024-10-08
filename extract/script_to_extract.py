import os
import pika
from dotenv import load_dotenv

load_dotenv()

host = os.getenv('RABBITMQ_HOST', '')
port = os.getenv('RABBITMQ_PORT', '')
exchange = os.getenv('EXCHANGE', '')
extract_links_queue = os.getenv('EXTRACT_LINKS', '')
extract_to_api_queue = os.getenv('EXTRACT_TO_API', '')
extract_links_dlq = os.getenv('EXTRACT_LINKS_DLQ', '')
extract_links_routing_key = os.getenv('EXTRACT_LINKS_ROUTING_KEY', '') 
extract_to_api_routing_key = os.getenv('EXTRACT_TO_API_ROUTING_KEY', '')
max_attempts = int(os.getenv('MAX_ATTEMPTS', 0))

ATTEMPTS_COUNT = os.getenv('ATTEMPTS_COUNT_HEADER', '')

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host, port)
)

def callback(ch, method, properties, body):
    try:
        #raise
        ch.basic_publish(
            exchange,
            extract_to_api_routing_key,
            body,
            pika.BasicProperties(headers = {
                ATTEMPTS_COUNT: 0
            })
        )
        print(f"Dados enviados para a fila '{extract_to_api_queue}'")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except:
        attempts = int(properties.headers[ATTEMPTS_COUNT])

        if attempts == max_attempts:
            print(f"O envio de mensagem falhou {max_attempts} vezes. Movendo para {extract_links_dlq}.")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        else:
            properties.headers[ATTEMPTS_COUNT] = attempts + 1
            ch.basic_publish(exchange,
                             extract_links_routing_key,
                             body,
                             pika.BasicProperties(headers=properties.headers))
            
            ch.basic_ack(delivery_tag=method.delivery_tag)

channel = connection.channel()
channel.basic_consume(extract_links_queue, callback)
channel.start_consuming()
