from dtos import TareaResponse
from fastapi import UploadFile
import shutil
import os
# import cv2


def save_video(video: UploadFile)-> TareaResponse:
    current_path = os.getcwd()
    path = f"{current_path}/videos/"
    file_path = f"{path}/{video.filename}"

    # procesar_video()

    if not os.path.exists(path):
        os.makedirs(path)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(video.file, buffer)

    return TareaResponse(id=1, estado="Procesando", url=file_path)


# def procesar_video():
#     current_path = os.getcwd()
#     nombre_video = "Bryan Adams - Heaven.mp4"

#     path = f"{current_path}/videos/{nombre_video}"
#     archivo_video = cv2.VideoCapture(path)

#     fps = archivo_video.get(cv2.CAP_PROP_FPS)
    
#     nombre_video_procesado = "Bryan Adams - Heaven-processed.mp4"
#     output_path = f"{current_path}/videos/{nombre_video_procesado}"
#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#     ancho = 360
#     alto = int(ancho * 9 / 19)

#     out = cv2.VideoWriter(output_path, fourcc, fps, (ancho, alto))
#     print("Live ******* 1")


#     frame_count = 0
#     while archivo_video.isOpened():
#         ret, frame = archivo_video.read()
#         if not ret:
#             break

#         # Check if we have reached 20 seconds (assuming 30 fps)
#         if frame_count >= 20 * fps:
#             break

#         # Write the processed frame to the output video
#         out.write(frame)

#         frame_count += 1

#     # Release the video capture and writer objects

#     print("*** Live ******* 2")
#     archivo_video.release()
#     out.release()



    