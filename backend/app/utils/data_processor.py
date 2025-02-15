import pandas as pd
import numpy as np
from typing import Optional

def process_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Procesa el dataset aplicando varias operaciones de limpieza
    
    Args:
        df (pd.DataFrame): DataFrame de entrada
        
    Returns:
        pd.DataFrame: DataFrame procesado
    """
    try:
        # Crear una copia para no modificar el original
        processed_df = df.copy()
        
        # 1. Limpieza básica
        # Eliminar filas duplicadas
        processed_df.drop_duplicates(inplace=True)
        
        # 2. Manejo de valores nulos
        # Identificar columnas numéricas y categóricas
        numeric_columns = processed_df.select_dtypes(include=[np.number]).columns
        categorical_columns = processed_df.select_dtypes(include=['object', 'category']).columns
        
        # Rellenar valores nulos
        for col in numeric_columns:
            # Usar la mediana para valores numéricos
            processed_df[col].fillna(processed_df[col].median(), inplace=True)
            
        for col in categorical_columns:
            # Usar el valor más frecuente para categóricos
            processed_df[col].fillna(processed_df[col].mode()[0], inplace=True)
        
        # 3. Manejo de outliers en columnas numéricas
        for col in numeric_columns:
            # Calcular Q1, Q3 e IQR
            Q1 = processed_df[col].quantile(0.25)
            Q3 = processed_df[col].quantile(0.75)
            IQR = Q3 - Q1
            
            # Definir límites
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            # Reemplazar outliers con los límites
            processed_df[col] = processed_df[col].clip(lower=lower_bound, upper=upper_bound)
        
        # 4. Normalización de texto para columnas categóricas
        for col in categorical_columns:
            # Convertir a minúsculas y eliminar espacios extra
            processed_df[col] = processed_df[col].str.lower().str.strip()
        
        # 5. Resetear el índice
        processed_df.reset_index(drop=True, inplace=True)
        
        # 6. Agregar metadatos del procesamiento
        processed_df.attrs['processing_info'] = {
            'rows_before': len(df),
            'rows_after': len(processed_df),
            'duplicates_removed': len(df) - len(processed_df),
            'columns_processed': list(processed_df.columns)
        }
        
        return processed_df
        
    except Exception as e:
        # En caso de error, loguear y re-levantar la excepción
        print(f"Error procesando el dataset: {str(e)}")
        raise

def get_dataset_summary(df: pd.DataFrame) -> dict:
    """
    Genera un resumen estadístico del dataset
    
    Args:
        df (pd.DataFrame): DataFrame a analizar
        
    Returns:
        dict: Diccionario con el resumen estadístico
    """
    summary = {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'null_counts': df.isnull().sum().to_dict(),
        'column_types': df.dtypes.astype(str).to_dict()
    }
    
    # Estadísticas para columnas numéricas
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    if len(numeric_columns) > 0:
        summary['numeric_stats'] = df[numeric_columns].describe().to_dict()
    
    # Estadísticas para columnas categóricas
    categorical_columns = df.select_dtypes(include=['object', 'category']).columns
    if len(categorical_columns) > 0:
        summary['categorical_stats'] = {
            col: df[col].value_counts().to_dict() 
            for col in categorical_columns
        }
    
    return summary