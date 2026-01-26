Ecommerce Data Pipeline
Pipeline automatizado ETL (Extract, Transform, Load) desarrollado en Python para extraer datos de ventas de una API, transformarlos con Pandas y almacenarlos en formato Parquet particionado de manera eficiente.

📂 Estructura del Proyecto
Plaintext
proyecto/

├── config.py           # Configuración (API Keys, URLs, constantes)

├── main.py             # Código principal del pipeline (ETL)

├── output/             # Directorio generado automáticamente

│   └── orders/         # Datos guardados particionados

│       ├── order_year=2025/

│       │   └── order_month=11/

│       │       └── part-0.parquet

│       └── ...

└── requirements.txt    # Librerías necesarias (pandas, requests, etc.)

🚀 Funcionalidades
1. Extracción Robusta (Extract)
Conexión a API REST segura mediante requests.

Sistema de Reintentos Inteligente: Implementa una estrategia de exponential backoff para manejar fallos de red o errores 5xx del servidor.

Manejo de excepciones específicas (Timeout, HTTPError, RequestException).

2. Transformación de Datos (Transform)
Conversión de JSON anidado a DataFrame de Pandas.

Limpieza de Fechas: Normalización de columnas de tiempo (order_date) eliminando horas innecesarias (00:00:00), manteniendo el tipo datetime64 para optimización.

Enriquecimiento: Creación automática de columnas order_year y order_month para la estrategia de particionado.

3. Carga Optimizada (Load)
Almacenamiento en formato Parquet (columnar y comprimido).

Particionado Hive-Style: Los datos se guardan organizados en carpetas jerárquicas por Año y Mes (year=X/month=Y) para optimizar futuras consultas y lecturas parciales.

🛠️ Requisitos Previos
Python 3.8+

Librerías listadas en requirements.txt:

Plaintext
pandas
requests
pyarrow
fastparquet (opcional, para engine de parquet)
⚙️ Configuración
Asegúrate de tener un archivo config.py en la raíz con tus credenciales:

Python
# config.py
API_KEY = "tu_api_key"
API_EMAIL = "tu_email"
API_BASE_URL = "https://api.tudominio.com"
▶️ Ejecución
Para correr el pipeline completo:

Bash
python main.py
El script generará logs detallados en la consola indicando el progreso de la extracción, la cantidad de filas procesadas y la ubicación final de los archivos.
