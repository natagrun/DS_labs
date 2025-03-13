import pika
import sys 

def send_message(message):
    # Подключение к локальному RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    
    # Создание очереди (если не существует)
    channel.queue_declare(queue='lab5_queue')
    
    # Отправка сообщения в очередь
    channel.basic_publish(
        exchange='',
        routing_key='lab5_queue',
        body=message
    )
    print(f" [x] Sent '{message}'")
    
    # Закрытие соединения
    connection.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python producer.py '<your_message>'")
        sys.exit(1)
    
    # Объединяем все аргументы (на случай, если сообщение содержит пробелы)
    message = ' '.join(sys.argv[1:])
    send_message(message)