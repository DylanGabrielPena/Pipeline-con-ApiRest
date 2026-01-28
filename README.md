🛒 Ecommerce Data Pipeline (🐳 Dockerized)
Pipeline automatizado ETL (Extract, Transform, Load) desarrollado en Python para extraer datos de ventas de una API, transformarlos con Pandas y almacenarlos en formato Parquet particionado de manera eficiente.

El proyecto ahora se encuentra Dockerizado, lo que garantiza que funcione en cualquier máquina sin necesidad de instalar Python ni librerías manualmente.

📂 Estructura del Proyecto
Plaintext
proyecto/

├── .env                   # 🔐 Variables de entorno (NO subir a Git)

├── .dockerignore          # Archivos que Docker debe ignorar

├── docker-compose.yml     # 🐳 Orquestación del contenedor y volúmenes

├── Dockerfile             # Receta para construir la imagen

├── config.py              # Lee la configuración desde variables de entorno

├── main.py                # Código principal del pipeline (ETL)

├── requirements.txt       # Dependencias (pandas, requests, pyarrow, etc.)

└── output/                # 📂 Directorio donde aparecen los datos (Mapeado via Volumen)
    └── orders/
        ├── order_year=2025/
        │   └── order_month=11/
        │       └── part-0.parquet
        └── ...
🚀 Funcionalidades
🔹 Extracción Robusta (Extract)
Conexión a API REST segura mediante requests.

Sistema de Reintentos Inteligente: Implementa exponential backoff para manejar fallos de red o errores 5xx.

Manejo de excepciones específicas (Timeout, HTTPError, RequestException).

🔹 Transformación de Datos (Transform)
Conversión de JSON anidado a DataFrame de Pandas.

Limpieza de Fechas: Normalización de columnas de tiempo (order_date).

Enriquecimiento: Creación automática de columnas order_year y order_month.

🔹 Carga Optimizada (Load)
Almacenamiento en formato Parquet (columnar y comprimido).

Particionado Hive-Style: Datos organizados jerárquicamente (year=X/month=Y) para consultas rápidas.

🔹 Infraestructura (Docker) [NUEVO]
Aislamiento: Ejecución en contenedor independiente.

Persistencia: Uso de Volúmenes de Docker para guardar los archivos generados en tu máquina local.

Seguridad: Inyección de credenciales mediante variables de entorno (.env), sin hardcodear claves en el código.

🛠️ Requisitos Previos
Docker Desktop (o Docker Engine + Compose) instalado.

No es necesario tener Python instalado localmente.

⚙️ Configuración
Clona el repositorio o descarga los archivos.

Crea un archivo llamado .env en la raíz del proyecto (junto al docker-compose.yml).

Agrega tus credenciales dentro del archivo .env:

Bash
# Archivo .env
API_KEY=tu_clave_secreta_real
API_EMAIL=tu_email@ejemplo.com
API_BASE_URL=https://api.tudominio.com
Nota: El archivo .env está en el .gitignore y .dockerignore para proteger tus claves. Nunca lo subas al repositorio.

▶️ Ejecución con Docker (Recomendado)
Para construir la imagen y ejecutar el pipeline:

Bash
docker-compose up --build
¿Qué sucederá?
Docker descargará las dependencias e iniciará el contenedor.

Verás los logs en la consola (Fetching data..., Procesando...).

Al finalizar, los archivos .parquet aparecerán automáticamente en tu carpeta local output/.

Comandos útiles
Detener y limpiar todo:

Bash
docker-compose down
Verificar variables cargadas (Debug):

Bash
docker-compose run --rm etl-ecommerce env
