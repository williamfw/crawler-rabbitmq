import pika
import mysql.connector
import json

# Configurações do RabbitMQ
rabbitmq_host = 'rabbitmq-crawler'
queue_name = 'noticias_queue'

# Configurações do MySQL
mysql_config: dict[str, str] = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'database': 'crawler',
    'charset':'utf8mb4'
}

# Conectar ao MySQL
def connect_mysql():
    return mysql.connector.connect(**mysql_config)

# Função para inserir um lote de mensagens no MySQL
def insert_batch_into_mysql(data_batch):
    # Conectar ao MySQL
    connection = connect_mysql()
    cursor = connection.cursor()

    # SQL para inserir os dados
    insert_query = """
    INSERT INTO noticias_g1 (titulo, subtitulo, datahora, autor, texto, link, legendas_imagens, links_imagens)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    # Inserir o lote no banco
    cursor.executemany(insert_query, data_batch)
    connection.commit()

    cursor.close()
    connection.close()

# Consumidor RabbitMQ
def callback(ch, method, properties, body):
    global message_batch

    try:
        # Converter o JSON recebido em um dicionário Python
        message = json.loads(body)

        # Adicionar a mensagem ao lote
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

        # Se o lote tiver 50 mensagens, insere no MySQL
        #if len(message_batch) >= 20:
        insert_batch_into_mysql(message_batch)
        print(f"Inserido lote de {len(message_batch)} mensagens no MySQL")
        message_batch.clear()  # Limpar o lote após inserir

        # Confirmação de que a mensagem foi processada
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except:
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

# Conectar ao RabbitMQ
def start_consuming():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost", port=5672)
    )

    channel = connection.channel()

    # Consumir da fila
    #channel.basic_qos(prefetch_count=20)
    channel.basic_consume(queue=queue_name, on_message_callback=callback)

    print("Aguardando mensagens da fila...")
    channel.start_consuming()

# Variável para armazenar o lote de mensagens
message_batch = []

if __name__ == '__main__':
    start_consuming()
