import datetime
from pydantic import BaseModel
from some_rabbitmq_library import send_message_to_rabbitmq, receive_message_from_rabbitmq

class Message(BaseModel):
    date: datetime.datetime
    msg: str

def send_message_rabbitmq(message: Message):
    send_message_to_rabbitmq(message.json())

def receive_last_message_rabbitmq():
    return receive_message_from_rabbitmq()
