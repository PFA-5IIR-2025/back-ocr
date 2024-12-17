FROM python:3.9-slim
RUN apt-get update && apt-get install -y tesseract-ocr
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY restApi.py /app/
WORKDIR /app
EXPOSE 5000
CMD ["python", "restApi.py"]
