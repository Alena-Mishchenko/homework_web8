from bson import json_util
from mongoengine import connect, Document, StringField,BooleanField, ReferenceField, ListField, CASCADE

connect(
    db="homework8",
    host="mongodb+srv://goitlearn:mypas@cluster0.nlahlds.mongodb.net/?retryWrites=true&w=majority",
)


class Contact(Document):
    fullname = StringField(required=True, unique=True)
    email = StringField(required=True,max_length=50)
    message_sent = BooleanField(default=False)  
    phone_number = StringField()
    address = StringField()
    prefered_communication = StringField(choices=["email", "sms"], default="email")
    meta = {"collection": "contact"}