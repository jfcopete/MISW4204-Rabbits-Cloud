import os
import cv2
from libs.cold_storage import crear_instancia_de_cloud_storage
from services.tarea import traer_tarea_por_id, actualizar_tarea

async def procesar_video(id: int):
    tarea = traer_tarea_por_id(id)

    if not tarea:
        return {"error": "Tarea no encontrada"}

    cold_storage = crear_instancia_de_cloud_storage()    
    cold_storage.download_file(id, tarea["nombre_archivo"])

    current_path = os.getcwd()
    logo = cv2.imread(f"{current_path}/img/IDRL.jpg", cv2.IMREAD_UNCHANGED)

    path = f"{current_path}/{tarea['nombre_archivo']}"
    archivo_video = cv2.VideoCapture(path)

    fps = archivo_video.get(cv2.CAP_PROP_FPS)
    
    nombre_video_procesado = f"editado_{tarea['nombre_archivo']}"
    output_path = f"{current_path}/{nombre_video_procesado}"
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    frame_ancho = int(archivo_video.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_alto = int(archivo_video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    nuevo_frame_alto = int(frame_alto * 9 / 16)
    
    salida = None
    logo_dimencionado = None
    try:
        salida = cv2.VideoWriter(output_path, fourcc, fps, (frame_ancho, nuevo_frame_alto))
        logo_dimencionado = cv2.resize(logo, (frame_ancho, frame_alto))
    except Exception as e:
        return {"error": "Error al crear el video procesado"}
    
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
        # Add keyframe interval
        if frame_count % int(fps) == 0:
            salida.set(cv2.VIDEOWRITER_PROP_QUALITY, 1)  # Forcing keyframe every second
        salida.write(frame_dimencionado)

        frame_count += 1

    archivo_video.release()
    salida.release()
    cold_storage.upload_file(id, nombre_video_procesado)

    borrar_archivos(tarea["nombre_archivo"])

    actualizar_tarea(id)

    return f"{current_path}/videos/{id}/{nombre_video_procesado}"


def borrar_archivos(nombre_archivo: str):
    os.remove(nombre_archivo)
    os.remove(f"editado_{nombre_archivo}")

