from fastapi import UploadFile
from dtos import TareaResponse
from servicios.tarea import crear_tarea, actualizar_tarea, actualizar_tarea_url
from servicios.kafka_services import send
import os
import cv2
from libs.cool_storage import crear_instancia_de_cloud_storage

# Servicio para cargar un video
async def save_video(video: UploadFile)-> TareaResponse:

    tarea_saved = crear_tarea(video.filename, "", "1")

    cool_storage = crear_instancia_de_cloud_storage()    
    file_path = cool_storage.upload_file(tarea_saved["id"], video)
    
    tarea = actualizar_tarea_url(tarea_saved['id'], file_path)

    #Enviar mensaje a kafka
    await send(tarea['id'])
    return TareaResponse(id=tarea['id'], estado="Procesando", url=file_path)

# Servicio para procesar un video
async def procesar_video(id: int):
    print(f"El id de la tarea es -> {id}")

    current_path = os.getcwd()
    logo = cv2.imread(f"{current_path}/img/IDRL.jpg", cv2.IMREAD_UNCHANGED)

    path = f"{current_path}/videos/{id}/original_{id}.mp4"
    archivo_video = cv2.VideoCapture(path)

    fps = archivo_video.get(cv2.CAP_PROP_FPS)
    
    nombre_video_procesado = "procesado.mp4"
    output_path = f"{current_path}/videos/{id}/{nombre_video_procesado}"
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    frame_ancho = int(archivo_video.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_alto = int(archivo_video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    nuevo_frame_alto = int(frame_alto * 9 / 16)

    salida = cv2.VideoWriter(output_path, fourcc, fps, (frame_ancho, nuevo_frame_alto))
    logo_dimencionado = cv2.resize(logo, (frame_ancho, frame_alto))

    frame_count = 0
    while archivo_video.isOpened():
        ret, frame = archivo_video.read()
        if not ret:
            break

        if frame_count < 2 * fps:
            frame[0:frame_alto, 0:frame_ancho] = logo_dimencionado

        if frame_count > 18 * fps:
            frame[0:frame_alto, 0:frame_ancho] = logo_dimencionado

        # Check if we have reached 20 seconds
        if frame_count >= 20 * fps:            
            break

        # Resize the frame 9:16 aspect ratio
        frame_dimencionado = cv2.resize(frame, (frame_ancho, nuevo_frame_alto))

        # Write the processed frame to the output video
        salida.write(frame_dimencionado)

        frame_count += 1

    # Release the video capture and writer objects
    archivo_video.release()
    salida.release()

    # Se actualiza el estado de la tarea al finalizar el procesamiento
    actualizar_tarea(id)
    return f"{current_path}/videos/{id}/{nombre_video_procesado}"

