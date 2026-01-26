import os
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv('API_KEY')
API_BASE_URL = os.getenv('API_BASE_URL', 'https://iansaura.com/api')
API_EMAIL = os.getenv('EMAIL')

if not API_KEY:
    raise ValueError("API_KEY no configurado. Creá un archivo .env")