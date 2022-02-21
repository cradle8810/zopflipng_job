import pika
import os

# 受信時コールバック関数
def callback(ch, method, properties, body):
    print(body.decode('utf-8'))
    ch.basic_ack(delivery_tag = method.delivery_tag)
    os._exit(0)

# 接続の作成
pika_param = pika.ConnectionParameters(host=os.environ.get('RABBITMQ'))
connection = pika.BlockingConnection(pika_param)

# チャンネルの作成
channel = connection.channel()

# キューの作成
channel.queue_declare(queue='before')

# 受信
channel.basic_qos(prefetch_count=1)
method_frame, header_frame, file_name = channel.basic_get('before')

# 1個読んでzopflipngに渡す
if method_frame:
    print(file_name.decode('utf-8'))
    channel.basic_ack(method_frame.delivery_tag)
else:
    print('No message returned')
    os._exit(1)

# 接続終了
channel.close()