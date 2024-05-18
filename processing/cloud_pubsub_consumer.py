from fastapi import APIRouter, HTTPException, Request
from procesar_video import procesar_video
import base64

router = APIRouter()

@router.post("/pubsub/push")
async def receive_message(request: Request):
    try:
        body = await request.json()
        message_data = body['message']['data']
        # Decode the base64 message data
        decoded_message_data = base64.b64decode(message_data).decode('utf-8')
        print(f"Received message: {decoded_message_data}")
        id = int(decoded_message_data)
        await procesar_video(id)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")