import os
import pika
from dotenv import load_dotenv
import queue_timer

load_dotenv()

host = os.getenv('RABBITMQ_HOST', '')
port = os.getenv('RABBITMQ_PORT', '')
exchange = os.getenv('EXCHANGE', '')
crawler_links_queue = os.getenv('CRAWLER_LINKS', '')
crawler_to_api_queue = os.getenv('CRAWLER_TO_API', '')
crawler_links_dlq = os.getenv('CRAWLER_LINKS_DLQ', '')
crawler_links_routing_key = os.getenv('CRAWLER_LINKS_ROUTING_KEY', '') 
crawler_to_api_routing_key = os.getenv('CRAWLER_TO_API_ROUTING_KEY', '')
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
            crawler_to_api_routing_key,
            body,
            pika.BasicProperties(headers = {
                ATTEMPTS_COUNT: 0
            })
        )
        print(f"Dados enviados para a fila '{crawler_to_api_queue}'")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except:
        attempts = int(properties.headers[ATTEMPTS_COUNT])

        if attempts == max_attempts:
            print(f"O envio de mensagem falhou {max_attempts} vezes. Movendo para {crawler_links_dlq}.")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        else:
            properties.headers[ATTEMPTS_COUNT] = attempts + 1
            ch.basic_publish(exchange,
                             crawler_links_routing_key,
                             body,
                             pika.BasicProperties(headers=properties.headers))
            
            ch.basic_ack(delivery_tag=method.delivery_tag)

try:
    channel = connection.channel()
    channel.basic_consume(crawler_links_queue, callback)
    channel.start_consuming()
finally:
    connection.close()
    print("Conexão encerrada. Terminal liberado.")