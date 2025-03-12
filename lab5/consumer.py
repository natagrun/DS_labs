import pika

def callback(ch, method, properties, body):
    print(f" [x] Received {body}")

def start_consumer():
    # Подключение к RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    
    # Создание очереди (если не существует)
    channel.queue_declare(queue='lab5_queue')
    
    # Настройка потребления сообщений
    channel.basic_consume(
        queue='lab5_queue',
        on_message_callback=callback,
        auto_ack=True
    )
    
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == "__main__":
    try:
        start_consumer()
    except KeyboardInterrupt:
        print("\nConsumer stopped")