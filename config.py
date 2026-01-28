import os

API_KEY = os.getenv('API_KEY')
API_BASE_URL = os.getenv('API_BASE_URL', 'https://iansaura.com/api')
API_EMAIL = os.getenv('API_EMAIL')


if not API_KEY:
    try:
        from dotenv import load_dotenv
        load_dotenv()
        API_KEY = os.getenv('API_KEY')
        API_EMAIL = os.getenv('API_EMAIL')
        API_BASE_URL = os.getenv('API_BASE_URL')
        print("se cargan valores localmente.")
    except ImportError:
        pass


if not API_KEY:
    raise ValueError("API_KEY no configurado. Creá un archivo .env")
if not API_EMAIL: 
    raise ValueError(f"API_EMAIL no configurado:{API_EMAIL} ")
