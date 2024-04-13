from dtos import TareaResponse
from fastapi import UploadFile
import shutil
import os
import cv2


def save_video(video: UploadFile)-> TareaResponse:
    current_path = os.getcwd()
    path = f"{current_path}/videos/"
    file_path = f"{path}/{video.filename}"

    print("start processing video")
    procesar_video("Bryan Adams - Heaven.mp4")
    print("end processing video")

    if not os.path.exists(path):
        os.makedirs(path)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(video.file, buffer)

    return TareaResponse(id=1, estado="Procesando", url=file_path)


def procesar_video(nombre_video: str):
    current_path = os.getcwd()
    logo = cv2.imread(f"{current_path}/img/logo.jpeg", cv2.IMREAD_UNCHANGED)

    path = f"{current_path}/videos/{nombre_video}"
    archivo_video = cv2.VideoCapture(path)

    fps = archivo_video.get(cv2.CAP_PROP_FPS)
    
    nombre_video_procesado = "heaven-processed.mp4"
    output_path = f"{current_path}/videos/{nombre_video_procesado}"
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
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
    # cv2.destroyAllWindows()



    