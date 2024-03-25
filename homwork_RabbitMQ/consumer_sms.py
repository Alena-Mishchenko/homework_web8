import json
import os
import sys
import pika
from models import Contact


credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='homework_exchange', exchange_type='direct')

channel.queue_declare(queue='sms_contacts', durable=True)
channel.queue_bind(exchange='homework_exchange', queue='sms_contacts', routing_key='sms')

def send_email(message):
    
    print(f"Sending email to {message}...")

def callback(ch, method, properties, body):
    contact_id = json.loads(body.decode())
    contact = Contact.objects.get(id=contact_id)
    if not contact.message_sent:
        # send_email(contact.email)
        contact.message_sent = True
        contact.save()
        print(f"Message sent to {contact.fullname}")
        # print(f" Received {contact_id}")
        # print(f" Completed {method.delivery_tag} task")
        # ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue='sms_contacts', on_message_callback=callback, auto_ack=True)
print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()      

   