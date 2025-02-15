from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
from io import StringIO
from .utils.data_processor import process_dataset
from .utils.storage import upload_to_gcs, generate_signed_url
from .config import Config

app = Flask(__name__)
# Configurar CORS para permitir todas las rutas
CORS(app, resources={r"/*": {"origins": "*"}})
app.config.from_object(Config)

@app.route('/process', methods=['POST'])
def process_data():
    try:
        # Verificar si se subió un archivo
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        # Leer el dataset
        df = pd.read_csv(file)
        
        # Procesar el dataset
        processed_df = process_dataset(df)
        
        # Verificar el tamaño del dataset
        memory_usage = processed_df.memory_usage(deep=True).sum()
        
        if memory_usage < 50 * 1024 * 1024:  # Si es menor a 50MB
            # Convertir a CSV en memoria
            output = StringIO()
            processed_df.to_csv(output, index=False)
            output.seek(0)
            
            return send_file(
                output,
                mimetype='text/csv',
                as_attachment=True,
                download_name='processed_dataset.csv'
            )
        else:
            # Subir a GCS y devolver URL firmada
            bucket_name = app.config['GCS_BUCKET']
            blob_name = f"processed/{file.filename}"
            
            # Subir archivo a GCS
            upload_to_gcs(processed_df, bucket_name, blob_name)
            
            # Generar URL firmada
            signed_url = generate_signed_url(bucket_name, blob_name)
            
            return jsonify({
                'message': 'Dataset processed successfully',
                'download_url': signed_url
            })

    except Exception as e:
        print(f"Error processing file: {str(e)}")  # Para debugging
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)