import pika
from mongoengine import connect
from models import Contact
import json
import sys
import os


# Підключення до MongoDB
connect(host="mongodb+srv://vrokmoitcattus:owtXMbGQIFr2444j@hw8.3qphtkz.mongodb.net/contacts_database?retryWrites=true&w=majority")

# Підключення до RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672))
channel = connection.channel()
channel.queue_declare(queue='contact_queue')

# Функція для обробки повідомлень з черги RabbitMQ
def callback(ch, method, properties, body):
    message = json.loads(body)
    contact_id = message.get('contact_id')
    if contact_id:
        contact = Contact.objects(id=contact_id).first()
        if contact:
            contact.message_sent = True
            contact.save()
            print(f" [x] Message sent for contact {contact_id}")
        else:
            print(f" [x] Contact with id {contact_id} not found")
    else:
        print(" [x] Invalid message format")

# Встановлення обробника повідомлень
channel.basic_consume(queue='contact_queue', on_message_callback=callback, auto_ack=True)

# Очікування повідомлень з черги RabbitMQ
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
try:
    channel.start_consuming()
except KeyboardInterrupt:
    print('Interrupted')
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)