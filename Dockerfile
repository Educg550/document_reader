FROM python:3.9-slim
EXPOSE 8501

RUN apt-get update && apt-get install -y \
    build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY read_image_text.py .
COPY .env .
COPY images/ images/
COPY texts/ texts/

ENTRYPOINT ["streamlit", "run"]
CMD ["read_image_text.py"]
