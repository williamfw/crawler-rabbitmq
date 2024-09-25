import pika
import mysql.connector
import json

rabbitmq_host = 'rabbitmq-crawler'
queue_name = 'noticias_queue'

mysql_config: dict[str, str] = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'database': 'crawler',
    'charset':'utf8mb4'
}

def connect_mysql():
    return mysql.connector.connect(**mysql_config)

def insert_batch_into_mysql(data_batch):
    connection = connect_mysql()
    cursor = connection.cursor()

    insert_query = """
    INSERT INTO noticias_g1 (titulo, subtitulo, datahora, autor, texto, link, legendas_imagens, links_imagens)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    cursor.executemany(insert_query, data_batch)
    connection.commit()

    cursor.close()
    connection.close()

def callback(ch, method, properties, body):
    global message_batch

    try:
        message = json.loads(body)

        data = (
            message['Título'],
            message['Subtítulo'],
            message.get('Data e Hora', None),
            message['Autor'],
            message.get('Texto', None).encode('ascii', 'ignore').decode('ascii'),
            message['Link'],
            message.get('Legendas Imagens', None),
            message.get('Links_imagens', None)
        )
        message_batch.append(data)

        insert_batch_into_mysql(message_batch)
        message_batch.clear()

        ch.basic_ack(delivery_tag=method.delivery_tag)
    except:
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

def start_consuming():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost", port=5672)
    )

    channel = connection.channel()

    channel.basic_consume(queue=queue_name, on_message_callback=callback)

    print("Aguardando mensagens da fila...")
    channel.start_consuming()

message_batch = []

if __name__ == '__main__':
    start_consuming()
