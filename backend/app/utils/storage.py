
from google.cloud import storage
import pandas as pd
from io import StringIO
import datetime

def upload_to_gcs(df: pd.DataFrame, bucket_name: str, blob_name: str) -> None:
    """
    Sube un DataFrame a Google Cloud Storage
    """
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    
    # Convertir DataFrame a CSV en memoria
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    
    # Subir el contenido
    blob.upload_from_string(csv_buffer.getvalue(), content_type='text/csv')

def generate_signed_url(bucket_name: str, blob_name: str) -> str:
    """
    Genera una URL firmada para descargar el archivo
    """
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    
    # Generar URL firmada válida por 1 hora
    url = blob.generate_signed_url(
        version="v4",
        expiration=datetime.timedelta(hours=1),
        method="GET"
    )
    
    return url