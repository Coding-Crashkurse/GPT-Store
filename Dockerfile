# Verwenden Sie ein offizielles Python-Image als Basis
FROM python:3.11

# Setzen Sie das Arbeitsverzeichnis im Container
WORKDIR /code

# Kopieren Sie die Abhängigkeiten und installieren Sie sie
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopieren Sie den Quellcode in den Container
COPY . .

# Startbefehl für die Anwendung
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]
