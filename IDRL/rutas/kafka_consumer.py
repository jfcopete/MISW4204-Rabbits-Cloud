# from fastapi import APIRouter, HTTPException
# from aiokafka import AIOKafkaConsumer
# from servicios.video import procesar_video
# import json
# import asyncio
# import time

# router = APIRouter()
# estado_consumidor = False  
# consumer = None  

# # Configura el consumidor de Kafka
# async def setup_kafka_consumer():
#     try:
#         consumer = AIOKafkaConsumer(
#             'task',
#             bootstrap_servers='35.192.59.87:9093',
#             group_id='my-group',
#             auto_offset_reset='earliest',
#             value_deserializer=lambda v: json.loads(v.decode('utf-8'))
#         )
#         await consumer.start()
#         try:
#             async for msg in consumer:
#                 if msg and msg.value:
#                     id = int(msg.value)
#                     await procesar_video(id)
#         except Exception as e:
#             print(f"Error processing Kafka messages: {str(e)}")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error initializing Kafka consumer: {str(e)}")

# loop = asyncio.get_event_loop()
# if loop.is_running():
#     asyncio.create_task(setup_kafka_consumer())
# else:
#     asyncio.run(setup_kafka_consumer())