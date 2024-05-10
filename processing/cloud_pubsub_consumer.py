from fastapi import APIRouter, HTTPException
from procesar_video import procesar_video
import json
import asyncio
from libs.cloud_pubsub import get_pubsub_instance

router = APIRouter()
estado_consumidor = False  
consumer = None  

# Configura el consumidor de cloud pubsub
async def setup_cloud_pubsub_consumer():
    try:
        pubsub_instance = get_pubsub_instance()

        def callback(message_data):
            id = int(message_data)
            asyncio.run(procesar_video(id))

        pubsub_instance.subscribe_to_messages(callback)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error initializing Pub/Sub consumer: {str(e)}")

loop = asyncio.get_event_loop()
if loop.is_running():
    asyncio.create_task(setup_cloud_pubsub_consumer())
else:
    asyncio.run(setup_cloud_pubsub_consumer())