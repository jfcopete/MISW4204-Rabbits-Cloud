FROM python:3.12-slim
WORKDIR /app
COPY almacenar_video.py /app/
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "almacenar_video.py"]