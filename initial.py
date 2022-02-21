import pika
import os

# RabbitMQへの接続
pika_param = pika.ConnectionParameters(host=os.environ.get('RABBITMQ'))
connection = pika.BlockingConnection(pika_param)
channel = connection.channel()
channel.queue_declare(queue='before')


file_list=os.listdir(path='.')

# メッセージの送信
for file in file_list:
    channel.basic_publish(exchange='',
        routing_key='before',
        body=file)

# 接続終了
channel.close()
