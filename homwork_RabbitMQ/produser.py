import json
import pika
from faker import Faker
from models import Contact


credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='homwork exchange', exchange_type='direct')
channel.queue_declare(queue='contacts_queue', durable=True)
channel.queue_bind(exchange='homwork exchange', queue='contacts_queue')


def create_contacts(nums: int):
    fake = Faker()
    contacts = []
    for _ in range(nums):
        contact = Contact(
            fullname=fake.name(),
            email=fake.email(),
            message_sent=False,
            phone_number=fake.phone_number(),
            address=fake.address()
        )
        contact.save()
        contacts.append(contact)
    return contacts

def send_contacts(contacts):
    for contact in contacts:
        message = str(contact.id)  
        channel.basic_publish(exchange='homwork exchange', routing_key='contacts_queue', body=json.dumps(message).encode())
    connection.close()



if __name__ == '__main__':
    fake_contacts = create_contacts(10)

    send_contacts(fake_contacts)

# fake = Faker()
# for _ in range(10): 
#     contact = Contact(
#         fullname=fake.name(),
#         email=fake.email(),
#         phone_number=fake.phone_number(),
#         address=fake.address().replace('\n', ', ')
#     )
#     contact.save()

#     # Додавання ObjectID контакту до черги RabbitMQ
#     channel.basic_publish(exchange='homwork exchange', routing_key='contact_queue', body=str(contact.id))

# connection.close()