from fastapi import UploadFile
from dtos import TareaResponse
from servicios.tarea import crear_tarea
from servicios.kafka_services import send
import shutil
import os
import cv2

async def save_video(video: UploadFile)-> TareaResponse:
    current_path = os.getcwd()
    path = f"{current_path}/videos/"

    if not os.path.exists(path):
        os.makedirs(path)

    existing_folders = [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]
    next_folder_name = str(len(existing_folders) + 1)
    video_folder = os.path.join(path, next_folder_name)
    os.makedirs(video_folder)

    file_path = os.path.join(video_folder, f"original_{next_folder_name}.mp4")

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(video.file, buffer)

    tarea = crear_tarea(video.filename, file_path, "1")
    print(f"Se ha creado la tarea desde el servicio de update video: {tarea['id']}")

    #Enviar mensaje a kafka
    await send(tarea['id'])
    return TareaResponse(id=tarea['id'], estado="Procesando", url=file_path)

# def procesar_video(nombre_video: str):
async def procesar_video(id: int):
    print(f"El id de la tarea es: {id}")

    current_path = os.getcwd()
    logo = cv2.imread(f"{current_path}/img/logo.jpeg", cv2.IMREAD_UNCHANGED)

    path = f"{current_path}/videos/{id}/original_{id}.mp4"
    print(path)
    archivo_video = cv2.VideoCapture(path)
    print(archivo_video)

    fps = archivo_video.get(cv2.CAP_PROP_FPS)
    
    nombre_video_procesado = "procesado.mp4"
    output_path = f"{current_path}/videos/{id}/{nombre_video_procesado}"
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    frame_ancho = int(archivo_video.get(cv2.CAP_PROP_FRAME_WIDTH))
    print("frame_ancho: ", frame_ancho)
    frame_alto = int(archivo_video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print("frame_alto: ", frame_alto)

    nuevo_frame_alto = int(frame_alto * 9 / 16)
    print("nuevo_frame_alto: ", nuevo_frame_alto)

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
    return f"{current_path}/videos/{id}/{nombre_video_procesado}"
    # cv2.destroyAllWindows()



    