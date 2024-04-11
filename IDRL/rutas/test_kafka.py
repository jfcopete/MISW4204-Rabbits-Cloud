from fastapi import APIRouter, status
from confluent_kafka import Producer

KAFKA_BOOTSTRAP_SERVERS = "kafka:9092"
KAFKA_TOPIC = "test_topic"

producer_config = {
    "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
}

producer = Producer(producer_config)
router = APIRouter()

@router.post("/test", status_code=status.HTTP_200_OK)
def test():
    message = "Mensaje de prueba"

    producer.produce(topic=KAFKA_TOPIC, value=message)
    return {"message": "Mensaje enviado a kafka"}