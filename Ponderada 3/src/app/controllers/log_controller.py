from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from services.messaging_service import send_message_rabbitmq, receive_last_message_rabbitmq, Message

router = APIRouter()

@router.post("/send-log", response_class=JSONResponse)
async def send_log(msg: Message):
    try:
        send_message_rabbitmq(msg)
        return JSONResponse(content={"message": "Log sent successfully!"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/receive-log")
async def receive_log():
    try:
        messages = []
        def callback(ch, method, properties, body):
            messages.append(body.decode())
            ch.basic_ack(delivery_tag=method.delivery_tag)
        
        receive_last_message_rabbitmq(callback)
        
        return JSONResponse(content={"messages": messages})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
