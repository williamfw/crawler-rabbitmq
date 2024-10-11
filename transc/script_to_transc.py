import os
import pika
from dotenv import load_dotenv
import queue_timer

load_dotenv()

host = os.getenv('RABBITMQ_HOST', '')
port = os.getenv('RABBITMQ_PORT', '')
exchange = os.getenv('EXCHANGE', '')
transc_links_queue = os.getenv('TRANSC_LINKS', '')
transc_to_api_queue = os.getenv('TRANSC_TO_API', '')
transc_links_dlq = os.getenv('TRANSC_LINKS_DLQ', '')
transc_links_routing_key = os.getenv('TRANSC_LINKS_ROUTING_KEY', '') 
transc_to_api_routing_key = os.getenv('TRANSC_TO_API_ROUTING_KEY', '')
max_attempts = int(os.getenv('MAX_ATTEMPTS', 0))

ATTEMPTS_COUNT = os.getenv('ATTEMPTS_COUNT_HEADER', '')

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host, port)
)

def stop_consuming():
    print(f"Encerrando a conexão após {queue_timer.TIMEOUT} segundos de inatividade.")
    channel.stop_consuming()

def callback(ch, method, properties, body):
    try:
        queue_timer.reset_timer(stop_consuming)
        ch.basic_publish(
            exchange,
            transc_to_api_routing_key,
            body,
            pika.BasicProperties(headers = {
                ATTEMPTS_COUNT: 0
            })
        )
        print(f"Dados enviados para a fila '{transc_to_api_queue}'")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except:
        attempts = int(properties.headers[ATTEMPTS_COUNT])

        if attempts == max_attempts:
            print(f"O envio de mensagem falhou {max_attempts} vezes. Movendo para {transc_links_dlq}.")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        else:
            properties.headers[ATTEMPTS_COUNT] = attempts + 1
            ch.basic_publish(exchange,
                             transc_links_routing_key,
                             body,
                             pika.BasicProperties(headers=properties.headers))
            
            ch.basic_ack(delivery_tag=method.delivery_tag)

try:
    channel = connection.channel()
    channel.basic_consume(transc_links_queue, callback)
    channel.start_consuming()
finally:
    connection.close()
    print("Conexão encerrada. Terminal liberado.")