# RabbitMQ Crawler

### diretório exchange
Diretório responsável por iniciar o serviço do RabbitMQ e criar as exchanges e filas. O arquivo .env tem duas variáveis que devem ser configuradas para rodar na Contabo:
- RABBITMQ_HOST=localhost
- RABBITMQ_PORT=5672

após iniciar o RabbitMQ, executar:
```bash
python3 create_queues.py
```

### diretório crawlers, extract, prints, transc
Os diretórios possuem exatamente a mesma estrutura. No arquivo .env tem algumas variáveis que devem ser configuradas para rodas na Contabo:
- URL_API=URL para ler os links
- URL_API_SAVE=URL para salvar na API
- RABBITMQ_HOST=
- RABBITMQ_PORT=
- MAX_ATTEMPTS=3 (numero de tentativas antes de cair na DLQ)
- TIMEOUT=15 (tempo de espera em segundos para encerrar a execução do script e liberar o terminal) 

após iniciar o container, executar:
```bash
python3 maker.py
python3 script_to_crawler.py
python3 script_to_api.py
```