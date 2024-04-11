from dtos import VideoResponse
from fastapi import UploadFile
import shutil
import os


def save_video(video: UploadFile)-> VideoResponse:
    current_path = os.getcwd()
    path = f"{current_path}/videos"
    file_path = f"{path}/{video.filename}"

    if not os.path.exists(f"{current_path}/videos/"):
        os.makedirs(f"{current_path}/videos/")

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(video.file, buffer)

    return VideoResponse(id=1, estado="Procesando", url=f'{path}/{video.filename}')
    