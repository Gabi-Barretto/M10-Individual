# app/services/__init__.py
from .messaging_service import send_message_rabbitmq, receive_last_message_rabbitmq, Message
from .image_service import remove_background_from_base64
