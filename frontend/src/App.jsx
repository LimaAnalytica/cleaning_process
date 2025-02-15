import React, { useState } from 'react';
import { Upload, FileUp, Download } from 'lucide-react';

const App = () => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [downloadUrl, setDownloadUrl] = useState('');
  const [success, setSuccess] = useState(false);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.type === 'text/csv') {
      setFile(selectedFile);
      setError('');
    } else {
      setError('Por favor, selecciona un archivo CSV válido');
      setFile(null);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Por favor, selecciona un archivo primero');
      return;
    }

    setLoading(true);
    setError('');
    setDownloadUrl('');
    setSuccess(false);

    const formData = new FormData();
    formData.append('file', file);

    try {
      // Usando la URL completa del backend
      const response = await fetch('http://localhost:5000/process', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Error al procesar el archivo');
      }

      const contentType = response.headers.get('content-type');
      if (contentType && contentType.includes('application/json')) {
        const data = await response.json();
        if (data.download_url) {
          setDownloadUrl(data.download_url);
        }
      } else {
        // Es una descarga directa
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        setDownloadUrl(url);
      }
      
      setSuccess(true);
    } catch (err) {
      console.error('Error details:', err);
      setError(err.message || 'Error al conectar con el servidor');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-2xl mx-auto">
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h1 className="text-2xl font-bold text-center mb-8">
              Procesador de Datasets
            </h1>

            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-6">
                <div className="flex flex-col items-center">
                  <Upload className="w-12 h-12 text-gray-400 mb-4" />
                  <label className="cursor-pointer">
                    <span className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition-colors">
                      Seleccionar Archivo CSV
                    </span>
                    <input
                      type="file"
                      accept=".csv"
                      onChange={handleFileChange}
                      className="hidden"
                    />
                  </label>
                  {file && (
                    <p className="mt-2 text-sm text-gray-600">
                      Archivo seleccionado: {file.name}
                    </p>
                  )}
                </div>
              </div>

              <button
                type="submit"
                disabled={loading || !file}
                className="w-full bg-green-500 text-white py-2 px-4 rounded hover:bg-green-600 transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed flex items-center justify-center gap-2"
              >
                {loading ? (
                  <>
                    <div className="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent" />
                    Procesando...
                  </>
                ) : (
                  <>
                    <FileUp className="w-5 h-5" />
                    Procesar Dataset
                  </>
                )}
              </button>
            </form>

            {error && (
              <div className="mt-4 p-4 bg-red-50 border border-red-200 text-red-700 rounded-md">
                {error}
              </div>
            )}

            {success && (
              <div className="mt-6">
                <div className="p-4 bg-green-50 text-green-700 border border-green-200 rounded-md">
                  Dataset procesado correctamente
                </div>
                {downloadUrl && (
                  <a
                    href={downloadUrl}
                    className="mt-4 flex items-center justify-center gap-2 bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 transition-colors"
                    download="processed_dataset.csv"
                  >
                    <Download className="w-5 h-5" />
                    Descargar Dataset Procesado
                  </a>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;