FROM python:3.9-slim
RUN apt-get update && \
    apt-get install -y tesseract-ocr && \
    apt-get install -y libgl1-mesa-glx && \
    apt-get clean

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY read_image_text.py .
COPY images/ images/
CMD ["python", "read_image_text.py"]
