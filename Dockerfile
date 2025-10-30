# Usa una imagen base de Python
FROM python:3.13-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de requirements.txt y los instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código al contenedor
COPY . .

# Expone el puerto en el que la aplicación escucha
ENV PORT= 8000
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
#CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]
