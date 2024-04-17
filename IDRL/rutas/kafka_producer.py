from fastapi import APIRouter, status
from aiokafka import AIOKafkaProducer
import json

router = APIRouter()

# Configura el productor de Kafka
producer = AIOKafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Inicializa el productor
async def setup_kafka_producer():
    await producer.start()

# Cierra el productor cuando la aplicación se detiene
async def close_kafka_producer():
    print("aqui se deberia cerrar el productor")
    pass
    #await producer.stop()

@router.post("/kafka", status_code=status.HTTP_201_CREATED)
async def send():
    await setup_kafka_producer()
    topic = 'test'
    message = {'hello': 'mensaje de prueba'}
    try:
        await producer.send_and_wait(topic, json.dumps(message))
        return {"mensaje_enviado": message}
    finally:
        await close_kafka_producer()