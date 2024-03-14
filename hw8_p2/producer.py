import pika
import faker
from mongoengine import connect
from models import Contact
import json

# Підключення до MongoDB
connect(host="mongodb+srv://vrokmoitcattus:owtXMbGQIFr2444j@hw8.3qphtkz.mongodb.net/contacts_database?retryWrites=true&w=majority")

# Підключення до RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672))
channel = connection.channel()
channel.queue_declare(queue='contact_queue')

# Генерування фейкових контактів
fake = faker.Faker()

def create_fake_contact():
    full_name = fake.name()
    email = fake.email()
    contact = Contact(full_name=full_name, email=email)
    contact.save()
    return contact

# Відправка контакту у чергу RabbitMQ
def send_contact_to_queue(contact):
    message = {
        'contact_id': str(contact.id)
    }
    channel.basic_publish(exchange='', routing_key='contact_queue', body=json.dumps(message))
    print(f" [x] Sent contact {contact.id} to queue")

if __name__ == "__main__":
    # Генеруємо та відправляємо 5 фейкових контактів
    for _ in range(5):
        contact = create_fake_contact()
        send_contact_to_queue(contact)

    # Закриваємо з'єднання з RabbitMQ
    connection.close()

