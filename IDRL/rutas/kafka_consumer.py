from fastapi import APIRouter, HTTPException
from aiokafka import AIOKafkaConsumer
from servicios.video import procesar_video
import json
import asyncio

router = APIRouter()
estado_consumidor = False  
consumer = None  

# Configura el consumidor de Kafka
async def setup_kafka_consumer():
    global consumer
    try:
        consumer = AIOKafkaConsumer(
            'task',
            bootstrap_servers='kafka:9092',
            group_id='my-group',
            auto_offset_reset='earliest',
            value_deserializer=lambda v: json.loads(v.decode('utf-8'))
        )
        await consumer.start()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error initializing Kafka consumer: {str(e)}")

# Cierra el consumidor cuando la aplicación se detiene
async def close_kafka_consumer():
    global consumer
    if consumer is not None:
        await consumer.stop()

# Endpoint para iniciar el consumidor de Kafka
@router.post("/start_consumer")
async def start_consumer():
    global estado_consumidor
    if not estado_consumidor:
        await setup_kafka_consumer()
        estado_consumidor = True
        return {"message": "Consumer started"}
    else:
        return {"message": "Consumer already started"}

# Lógica para procesar los mensajes recibidos
async def process_messages():
    global consumer
    try:
        async for msg in consumer:
            tarea_id = int(msg.value.split(" ")[1].replace("}", ""))
            print("que soy", tarea_id)
            await procesar_video(tarea_id)
    except Exception as e:
        print(f"Error processing Kafka messages: {str(e)}")

# Ejecuta el consumidor de Kafka en segundo plano
@router.on_event("startup")     
async def startup_event():
    global estado_consumidor
    try:
        await start_consumer()
        asyncio.create_task(process_messages())
    except Exception as e:
        print(f"Error starting up: {str(e)}")

# Endpoint para detener el consumidor de Kafka
@router.post("/stop_consumer")
async def stop_consumer():
    global estado_consumidor
    if estado_consumidor:
        await close_kafka_consumer()
        estado_consumidor = False
        return {"message": "Consumer stopped"}
    else:
        return {"message": "Consumer already stopped"}
