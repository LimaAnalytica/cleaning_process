import os

class Config:
    GCS_BUCKET = os.getenv('GCS_BUCKET', 'my-datasets-bucket')
    PROJECT_ID = os.getenv('PROJECT_ID', 'my-project-id')

# app/utils/data_processor.py
import pandas as pd

def process_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Función para procesar el dataset
    Aquí puedes agregar tu lógica específica de limpieza
    """
    # Ejemplo de procesamiento básico
    processed_df = df.copy()
    
    # Eliminar filas duplicadas
    processed_df.drop_duplicates(inplace=True)
    
    # Eliminar filas con valores nulos
    processed_df.dropna(inplace=True)
    
    # Resetear el índice
    processed_df.reset_index(drop=True, inplace=True)
    
    return processed_df
