#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Programa para extrair informações sobre notícias do g1 (título, subtítulo, data, autor e descrição)

import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import pandas as pd
import json
import pika

# URL do RSS
rss_url = 'https://g1.globo.com/rss/g1/'

requisicao = requests.get(rss_url)

site = BeautifulSoup(requisicao.text, "html.parser")
#print(site.prettify())


# In[2]:


# Encontra todos os itens da página
itens = site.find_all("item")

links = []

# Busca os links de cada matéria e salva numa lista
for item in itens:
    links.append(item.find('guid').text)    

#links = ['https://g1.globo.com/df/distrito-federal/noticia/2024/09/17/policia-civil-cria-forca-tarefa-para-investigar-suspeita-de-incendios-criminosos-no-df.ghtml']
# In[3]:


# Padrões a serem removidos:
patterns_to_remove = ['🔔','📲','✅','📳','📱', 'LEIA TAMBÉM', 'LEIA MAIS', 'Leia mais', 'Vídeos mais assistidos',                      'Veja os vídeos mais assistidos', 'Veja os vídeos mais recentes', 'Assista a mais notícias',
                      'Siga o g1 no Instagram', 'Receba as notícias no WhatsApp', 'Veja outras notícias', 
                      'Assista aos vídeos', 'Veja o plantão de últimas notícias', 'Veja mais notícias', 'REVEJA VÍDEOS',
                      'Siga, curta ou assine', 'Ouça os podcasts', 'Veja vídeos', 'Leia outras notícias', 
                      'Veja mais', 'VÍDEOS com as notícias', 'Mais assistidos do g1', 'Confira mais notícias',
                      'Confira outras notícias', 'Acompanhe o canal do g1', 'Clique aqui e saiba mais',\
                      'Leia mais', 'Participe do canal do g1', 'Assista aos vídeos mais vistos', 'Siga o g1', 'VÍDEOS',
                      'Leia também', 'Assista:', 'Siga o canal g1', 'Vídeos:', 'VEJA TAMBÉM', 'Vídeos mais vistos', 
                      'Vídeos do Leste', 'Vídeos do Norte', 'Vídeos do Sul', 'Vídeos do Sudeste', 'Vídeos do Nordeste',
                      'Videos do Centroeste', 'Vídeos do Oeste', 'Reveja os telejornais', 'Veja os telejornais']

news_data = [] # Lista de notícias

# Acessa cada link da página para buscar as informações
for link in links:    
    requisicao = requests.get(link)
    site = BeautifulSoup(requisicao.text, "html.parser")
    try:
        titulo_element = site.find(class_='content-head__title')
        titulo = titulo_element.text if titulo_element else ''# Busca o título da matéria
        print('Título:', titulo, '\n')        
        subtitulo_element = site.find(class_='content-head__subtitle')
        subtitulo = subtitulo_element.text if subtitulo_element else '' # Busca o subtítulo da matéria
        print('Subtítulo:', subtitulo, '\n')
        
        # Entra no artigo propriamente dito
        artigo = site.find('article')
        if artigo is not None:
            # Obtem uma lista contendo todos os conteúdos de texto espalhados pelo artigo
            descricoes = artigo.find_all(class_='content-text__container')
            if descricoes != []: # Caso o artigo possua conteúdo de texto
                descricao_completa = ''
                for descricao in descricoes:
                    if descricao.find(class_='content-unordered-list'): # Verifica se há lista de conteúdos 
                        if descricao.find(class_='content-unordered-list').find_all('a', href=True): # Caso sejam lista com links
                            pass
                        else: # Caso sejam listas sobre conteúdos
                            descricao_completa += descricao.text            
                    elif any(pattern in descricao.text for pattern in patterns_to_remove): # Remove propagandas
                        pass
                    else:
                        descricao_completa += descricao.text                
            else:
                descricao_completa = ''
            
            print('Descrição:', descricao_completa, '\n')       
            
            # Obtem uma lista contendo todas as informações sobre as imagens espalhados pelo artigo
            imagens = artigo.find_all(class_='content-media-image')
            if imagens != []: # Cajo hajam imagens no artigo 
                legendas_imagens = ''
                links_imagens = ''
                for imagem in imagens:
                    legendas_imagens += imagem.get('alt') + ',' + ' '# Extrai a legenda da imagem 
                    links_imagens += imagem.get('src') + ' ,' + ' ' # Extrai o link da imagem
                    print('Legendas imagens:', legendas_imagens, '\n')
                    print('Links imagens:', links_imagens, '\n')
            else: # Cajo não hajam imagens no artigo 
                legendas_imagens = ''
                links_imagens = ''
        
        # Extrai as informações de auto e data 
        from_element = site.find(class_='content-publication-data__from')
        autor = from_element.text if from_element else ''
        print('Autor:', autor, '\n')
        
        data_element = site.find(class_='content-publication-data__updated')
        data = data_element.text if data_element else ''
        print('Data:', data, '\n') 
        
    except AttributeError:
        descricao_completa = ''
        legendas_imagens = ''
        links_imagens = ''
        print('Abortando execução do extrator')
        exit()
                        
     # Adicionar os dados à lista de notícias
    news_item = {
        'Título': titulo,
        'Subtítulo': subtitulo,
        'Data e Hora': data,
        'Autor': autor,
        'Texto': descricao_completa,
        'Link' : link,
        'Legendas Imagens': legendas_imagens,
        'Links_imagens' : links_imagens
    }
    news_data.append(news_item)


# In[4]:


# Converter os dados para um DataFrame do pandas
df = pd.DataFrame(news_data)

# Remover as linhas onde as colunas 'Texto' e 'Legendas Imagens' estão vazias
df = df[~((df['Texto'] == '') & (df['Legendas Imagens'] == ''))]

#display(df)


# In[5]:


# Obter a data e a hora atual
data_hora_atual = datetime.now()

# Converter o DataFrame para um dicionário de registros
data_json = df.to_dict(orient='records')

# Salvar os dados do DataFrame em um arquivo JSON
#output_file = 'noticias_g1_' + str(data_hora_atual).replace(' ','_').replace('.','').replace(':','') + '.json'

#ith open(output_file, 'w', encoding='utf-8') as f:
#    json.dump(data_json, f, ensure_ascii=False, indent=4)

#print(f"As informações foram salvas no arquivo JSON: {output_file}")


# In[ ]:


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", port=5672)
)

channel = connection.channel()

# Declarar a Dead Letter Exchange (DLX)
channel.exchange_declare(exchange='dlx_exchange', exchange_type='direct')

# Declarar a Dead Letter Queue (DLQ)
channel.queue_declare(queue='dlq')

# Vincular a DLQ à DLX
channel.queue_bind(exchange='dlx_exchange', queue='dlq', routing_key='dlq_routing_key')

channel.exchange_declare(
    exchange='crawler_exchange',
    exchange_type='direct', 
    durable=True
)

channel.queue_declare(
    queue='noticias_queue',
    arguments={
        'x-dead-letter-exchange': 'dlx_exchange',
        'x-dead-letter-routing-key': 'dlq_routing_key',
        'x-max-length': 1000  # (opcional) Tamanho máximo da fila antes de mover para DLQ
    }
)

channel.queue_bind(
    exchange='crawler_exchange',
    queue='noticias_queue',
    routing_key='noticias_g1'
)



for json_content in data_json:
    channel.basic_publish(exchange="crawler_exchange", routing_key="noticias_g1", body=json.dumps(json_content))

connection.close()
