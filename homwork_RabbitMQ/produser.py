import json
import pika
from faker import Faker
from models import Contact


credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='homwork exchange', exchange_type='direct')
# channel.queue_declare(queue='contacts_queue', durable=True)
# channel.queue_bind(exchange='homwork exchange', queue='contacts_queue')

channel.queue_declare(queue='email_contacts', durable=True)
channel.queue_bind(exchange='homework_exchange', queue='email_contacts', routing_key='email')

# Queue for SMS contacts
channel.queue_declare(queue='sms_contacts', durable=True)
channel.queue_bind(exchange='homework_exchange', queue='sms_contacts', routing_key='sms')
def create_contacts(nums: int):
    fake = Faker()
    contacts = []
    for _ in range(nums):
        contact = Contact(
            fullname=fake.name(),
            email=fake.email(),
            message_sent=False,
            phone_number=fake.phone_number(),
            # address=fake.address()
            prefered_communication=fake.random_element(elements=["email", "sms"])
        )
        contact.save()
        contacts.append(contact)
    return contacts

def send_contacts(contacts):
    for contact in contacts:
        message = str(contact.id)  
        # channel.basic_publish(exchange='homwork exchange',\
        #  routing_key='contacts_queue', body=json.dumps(message).encode())
        routing_key = 'email' if contact.prefered_communication == 'email' else 'sms'
        channel.basic_publish(exchange='homework_exchange', routing_key=routing_key, body=json.dumps(message).encode())
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