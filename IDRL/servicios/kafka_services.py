from aiokafka import AIOKafkaProducer
import json

producer = AIOKafkaProducer(
    bootstrap_servers='104.197.98.214:9093',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Inicializa el productor
async def setup_kafka_producer():
    await producer.start()

# Cierra el productor cuando la aplicación se detiene
async def close_kafka_producer():
    print("instrucción de cerrar el productor")
    await producer.stop()

async def send(idTask :int):
    print("**** mensaje enviado desde el productor de kafka_services ****")
    await setup_kafka_producer()
    topic = 'task'
    message = idTask
    try:
        await producer.send_and_wait(topic, json.dumps(message))
        return {"mensaje_enviado": message}
    finally:
        return {"mensaje_enviado": message}