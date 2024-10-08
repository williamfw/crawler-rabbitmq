import os
import pika
from pika.exchange_type import ExchangeType
from dotenv import load_dotenv

load_dotenv()

host = os.getenv('RABBITMQ_HOST', '')
port = os.getenv('RABBITMQ_PORT', '')
exchange = os.getenv('EXCHANGE', '')
dlx = os.getenv('DLX', '')

# EXTRATORES
extract_links_queue = os.getenv('EXTRACT_LINKS', '')
extract_links_dlq = os.getenv('EXTRACT_LINKS_DLQ', '')
extract_to_api_queue = os.getenv('EXTRACT_TO_API', '')
extract_to_api_dlq = os.getenv('EXTRACT_TO_API_DLQ', '')

extract_links_routing_key = os.getenv('EXTRACT_LINKS_ROUTING_KEY', '')
extract_links_dlq_routing_key = os.getenv('EXTRACT_LINKS_DLQ_ROUTING_KEY', '')
extract_to_api_routing_key = os.getenv('EXTRACT_TO_API_ROUTING_KEY', '')
extract_to_api_dlq_routing_key = os.getenv('EXTRACT_TO_API_DLQ_ROUTING_KEY', '')

# CRAWLER
crawler_links_queue = os.getenv('CRAWLER_LINKS', '')
crawler_links_dlq = os.getenv('CRAWLER_LINKS_DLQ', '')
crawler_to_api_queue = os.getenv('CRAWLER_TO_API', '')
crawler_to_api_dlq = os.getenv('CRAWLER_TO_API_DLQ', '')

crawler_links_routing_key = os.getenv('CRAWLER_LINKS_ROUTING_KEY', '')
crawler_links_dlq_routing_key = os.getenv('CRAWLER_LINKS_DLQ_ROUTING_KEY', '')
crawler_to_api_routing_key = os.getenv('CRAWLER_TO_API_ROUTING_KEY', '')
crawler_to_api_dlq_routing_key = os.getenv('CRAWLER_TO_API_DLQ_ROUTING_KEY', '')

# TRANSCRIÇÃO
transc_files_queue = os.getenv('TRANSC_FILES', '')
transc_files_dlq = os.getenv('TRANSC_FILES_DLQ','')
transc_to_api_queue = os.getenv('TRANSC_TO_API', '')
transc_to_api_dlq = os.getenv('TRANSC_TO_API_DLQ', '')

transc_files_routing_key = os.getenv('TRANSC_FILES_ROUTING_KEY', '')
transc_files_dlq_routing_key = os.getenv('TRANSC_FILES_DLQ_ROUTING_KEY','')
transc_to_api_routing_key = os.getenv('TRANSC_TO_API_ROUTING_KEY', '')
transc_to_api_dlq_routing_key = os.getenv('TRANSC_TO_API_DLQ_ROUTING_KEY', '')

# PRINTS
print_links_queue = os.getenv('PRINT_LINKS', '')
print_links_dlq = os.getenv('PRINT_LINKS_DLQ', '')
print_to_api_queue = os.getenv('PRINT_TO_API', '')
print_to_api_dlq = os.getenv('PRINT_TO_API_DLQ', '')

print_links_routing_key = os.getenv('PRINT_LINKS_ROUTING_KEY', '')
print_links_dlq_routing_key = os.getenv('PRINT_LINKS_DLQ_ROUTING_KEY', '')
print_to_api_routing_key = os.getenv('PRINT_TO_API_ROUTING_KEY', '')
print_to_api_dlq_routing_key = os.getenv('PRINT_TO_API_DLQ_ROUTING_KEY', '')

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host, port)
)

channel = connection.channel()
channel.exchange_declare(exchange, ExchangeType.direct)
channel.exchange_declare(dlx, ExchangeType.direct)

#declarações de filas e bind para exchange de extract
channel.queue_declare(extract_links_queue, durable=True, arguments={
    'x-dead-letter-exchange': dlx,
    'x-dead-letter-routing-key': extract_links_dlq_routing_key
})
channel.queue_declare(extract_links_dlq, durable=True)
channel.queue_declare(extract_to_api_queue, durable=True, arguments={
    'x-dead-letter-exchange': dlx,
    'x-dead-letter-routing-key': extract_to_api_dlq_routing_key
})
channel.queue_declare(extract_to_api_dlq, durable=True)

channel.queue_bind(extract_links_queue, exchange, extract_links_routing_key)
channel.queue_bind(extract_links_dlq, dlx, extract_links_dlq_routing_key)
channel.queue_bind(extract_to_api_queue, exchange, extract_to_api_routing_key)
channel.queue_bind(extract_to_api_dlq, dlx, extract_to_api_dlq_routing_key)

#declarações de filas e bind para exchange de crawler
channel.queue_declare(crawler_links_queue, durable=True, arguments={
    'x-dead-letter-exchange': dlx,
    'x-dead-letter-routing-key': crawler_links_dlq_routing_key
})
channel.queue_declare(crawler_links_dlq, durable=True)
channel.queue_declare(crawler_to_api_queue, durable=True, arguments={
    'x-dead-letter-exchange': dlx,
    'x-dead-letter-routing-key': crawler_to_api_dlq_routing_key
})
channel.queue_declare(crawler_to_api_dlq, durable=True)

channel.queue_bind(crawler_links_queue, exchange, crawler_links_routing_key)
channel.queue_bind(crawler_links_dlq, dlx, crawler_links_dlq_routing_key)
channel.queue_bind(crawler_to_api_queue, exchange, crawler_to_api_routing_key)
channel.queue_bind(crawler_to_api_dlq, dlx, crawler_to_api_dlq_routing_key)

#declarações de filas e bind para exchange de transcrição
channel.queue_declare(transc_files_queue, durable=True, arguments={
    'x-dead-letter-exchange': dlx,
    'x-dead-letter-routing-key': transc_files_dlq_routing_key
})
channel.queue_declare(transc_files_dlq, durable=True)
channel.queue_declare(transc_to_api_queue, durable=True, arguments={
    'x-dead-letter-exchange': dlx,
    'x-dead-letter-routing-key': transc_to_api_dlq_routing_key
})
channel.queue_declare(transc_to_api_dlq, durable=True)

channel.queue_bind(transc_files_queue, exchange, transc_files_routing_key)
channel.queue_bind(transc_files_dlq, dlx, transc_files_dlq_routing_key)
channel.queue_bind(transc_to_api_queue, exchange, transc_to_api_routing_key)
channel.queue_bind(transc_to_api_dlq, dlx, transc_to_api_dlq_routing_key)

#declarações de filas e bind para exchange de print
channel.queue_declare(print_links_queue, durable=True, arguments={
    'x-dead-letter-exchange': dlx,
    'x-dead-letter-routing-key': print_links_dlq_routing_key
})
channel.queue_declare(print_links_dlq, durable=True)
channel.queue_declare(print_to_api_queue, durable=True, arguments={
    'x-dead-letter-exchange': dlx,
    'x-dead-letter-routing-key': print_to_api_dlq_routing_key
})
channel.queue_declare(print_to_api_dlq, durable=True)

channel.queue_bind(print_links_queue, exchange, print_links_routing_key)
channel.queue_bind(print_links_dlq, dlx, print_links_dlq_routing_key)
channel.queue_bind(print_to_api_queue, exchange, print_to_api_routing_key)
channel.queue_bind(print_to_api_dlq, dlx, print_to_api_dlq_routing_key)
