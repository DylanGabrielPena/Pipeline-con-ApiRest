FROM python:3.9-slim

WORKDIR /app

# 1. Primero copiamos solo los requerimientos (para aprovechar el caché)
COPY requirements.txt .

# 2. Instalamos las librerías
RUN pip install -r requirements.txt

# 3. Recién ahora copiamos el código fuente
COPY . .

# 4. Ejecutamos
CMD ["python", "main.py"]