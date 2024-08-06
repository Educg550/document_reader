FROM python:3.9-slim
RUN apt-get update && \
    apt-get clean

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY read_image_text.py .
COPY images/ images/
COPY texts/ texts/
CMD ["python", "read_image_text.py"]
