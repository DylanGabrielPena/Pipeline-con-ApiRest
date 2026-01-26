import requests
from config import API_KEY,API_BASE_URL,API_EMAIL
import logging
import time
from requests.exceptions import RequestException, Timeout, HTTPError
import pandas as pd
import json
import os

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def fetch_data(dataset_type: str = 'ecommerce', rows: int = 1000) -> dict:
    """Obtiene datos de la API."""
    url = f"{API_BASE_URL}/datasets.php"
    params = {
        'email':API_EMAIL,
        'key':API_KEY,
        'type': dataset_type,
        'rows': rows,
        }
    
    logger.info(f"Fetching {rows} rows of {dataset_type} data...")
    
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()  # Lanza excepción si hay error HTTP
    
    data = response.json()
    logger.info(f"Received {len(data.get('tables', {}).get('orders', []))} orders")
    
    return data


def fetch_data_with_retry(
    dataset_type: str = 'ecommerce', 
    rows: int = 1000,
    max_retries: int = 3,
    backoff_factor: float = 2.0
) -> dict:
    """Obtiene datos con reintentos automáticos."""
    
    for attempt in range(max_retries):
        try:
            return fetch_data(dataset_type, rows)
            
        except Timeout:
            logger.warning(f"Timeout en intento {attempt + 1}/{max_retries}")
            
        except HTTPError as e:
            if e.response.status_code >= 500:
                logger.warning(f"Error del servidor: {e}")
            else:
                # Errores 4xx no se reintentan
                logger.error(f"Error del cliente: {e}")
                raise
                
        except RequestException as e:
            logger.warning(f"Error de conexión: {e}")
        
        if attempt < max_retries - 1:
            wait_time = backoff_factor ** attempt
            logger.info(f"Reintentando en {wait_time} segundos...")
            time.sleep(wait_time)
    
    raise Exception(f"Falló después de {max_retries} intentos")


def transform_data(data)-> pd.DataFrame:
    orders= data.get("tables").get("orders")
    df_orders= pd.DataFrame(orders)
    #print(df_orders.isnull().sum())  Se revisaron los nulos.
    #print(df_orders.dtypes) se revisaron los tipos de las columnas

    df_orders["order_date"] = pd.to_datetime(df_orders['order_date']).dt.normalize()
    df_orders["order_year"] = df_orders['order_date'].dt.year
    df_orders["order_month"] = df_orders["order_date"].dt.month
    
    return df_orders


def guardar_df(df, output_dir):
    
    logger.info(f"Guardando datos en {output_dir}...")
    os.makedirs(output_dir, exist_ok=True)
    
    # Guardar particionado por mes
    df.to_parquet(
        f'{output_dir}/orders',
        partition_cols=['order_year', 'order_month'],
        index=False
    )
    
    # Se guarda la opcion de dejarlo en 1 solo lugar.
    #df.to_parquet(f'{output_dir}/orders_all.parquet', index=False)
    
    # Estadísticas
    logger.info(f"Guardadas {len(df)} órdenes")
    logger.info(f"Particiones: {df['order_month'].nunique()} meses")



def orquestador():
    try:
        logger.info("Inicio de proceso")
        #Extraccion
        data=fetch_data_with_retry("ecommerce",3000)

        #Transformacion
        df=transform_data(data)

        if df.empty:
            logger.error("El DataFrame no tiene informacion")
            
        #cargar
        guardar_df(df,"output/")

        logger.info("Fin de proceso")
    except Exception as e:
        logger.error(f"Pipeline falló: {e}")
        raise


if __name__ == "__main__":
   orquestador()

    
    
   

   