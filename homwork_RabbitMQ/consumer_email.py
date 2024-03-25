import pika
import json
from models import Contact

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='homework_exchange', exchange_type='direct')

channel.queue_declare(queue='email_contacts', durable=True)
channel.queue_bind(exchange='homework_exchange', queue='email_contacts', routing_key='email')

def callback(ch, method, properties, body):
    contact_id = json.loads(body.decode())
    contact = Contact.objects.get(id=contact_id)
    if not contact.message_sent:
        # Implement email sending logic here
        # send_email(contact.email)
        contact.message_sent = True
        contact.save()
        print(f"Email sent to {contact.full_name}")

channel.basic_consume(queue='email_contacts', on_message_callback=callback, auto_ack=True)
print('Waiting for email contacts...')
channel.start_consuming()