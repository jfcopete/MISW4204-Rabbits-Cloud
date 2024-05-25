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
    logo_path = f"{current_path}/img/IDRL.jpg"
    
    if not os.path.isfile(logo_path):
        return {"error": "Logo file not found"}
    
    logo = cv2.imread(logo_path, cv2.IMREAD_UNCHANGED)

    video_path = f"{current_path}/{tarea['nombre_archivo']}"
    
    if not os.path.isfile(video_path):
        return {"error": "Video file not found"}
    
    archivo_video = cv2.VideoCapture(video_path)

    if not archivo_video.isOpened():
        return {"error": "Cannot open video file"}

    fps = archivo_video.get(cv2.CAP_PROP_FPS)
    
    nombre_video_procesado = f"editado_{tarea['nombre_archivo']}"
    output_path = f"{current_path}/{nombre_video_procesado}"
    fourcc = cv2.VideoWriter_fourcc(*"mp4v") 
    frame_ancho = int(archivo_video.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_alto = int(archivo_video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    nuevo_frame_alto = int(frame_ancho * 9 / 16)
    
    if nuevo_frame_alto % 2 != 0:
        nuevo_frame_alto += 1

    try:
        salida = cv2.VideoWriter(output_path, fourcc, fps, (frame_ancho, nuevo_frame_alto))
        logo_dimencionado = cv2.resize(logo, (frame_ancho, frame_alto))
    except Exception as e:
        return {"error": f"Error al crear el video procesado: {e}"}
    
    frame_count = 0
    while archivo_video.isOpened():
        ret, frame = archivo_video.read()
        if not ret:
            break

        if frame_count < 2 * fps:
            frame[0:frame_alto, 0:frame_ancho] = logo_dimencionado

        if frame_count > 18 * fps:
            frame[0:frame_alto, 0:frame_ancho] = logo_dimencionado

        if frame_count >= 20 * fps:
            break

        frame_dimencionado = cv2.resize(frame, (frame_ancho, nuevo_frame_alto))

        salida.write(frame_dimencionado)

        frame_count += 1

    archivo_video.release()
    salida.release()
    
    try:
        cold_storage.upload_file(id, nombre_video_procesado)
    except Exception as e:
        return {"error": f"Error al subir el video procesado: {e}"}

    borrar_archivos(video_path, output_path)

    actualizar_tarea(id)

    return f"{current_path}/{nombre_video_procesado}"


def borrar_archivos(*archivos: str):
    for archivo in archivos:
        if os.path.isfile(archivo):
            os.remove(archivo)