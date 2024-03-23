import json
import os
import sys
import pika
from models import Contact


credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='homwork_queue', durable=True)

def send_email(message):
    
    print(f"Sending email to {message}...")

def callback(ch, method, properties, body):
    contact_id = json.loads(body.decode())
    contact = Contact.objects.get(id=contact_id)
    if not contact.message_sent:
        send_email(contact.email)
        contact.message_sent = True
        contact.save()
        print(f"Message sent to {contact.fullname}")
        # print(f" Received {contact_id}")
        # print(f" Completed {method.delivery_tag} task")
        # ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue='contacts_queue', on_message_callback=callback, auto_ack=True)
print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()      

   

    # channel.basic_qos(prefetch_count=1)



# if __name__ == '__main__':
#     try:
#         main()
#     except KeyboardInterrupt:
#         print('Interrupted')
#         try:
#             sys.exit(0)
#         except SystemExit:
#             os._exit(0)