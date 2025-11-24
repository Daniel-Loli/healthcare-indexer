import azure.functions as func
import logging
import os
import requests
import time

app = func.FunctionApp()

# ============================================================
#   BLOB TRIGGER — SOLO ACTIVA EL INDEXADOR
# ============================================================

@app.blob_trigger(
    arg_name="myblob",
    path="docs/{name}", 
    connection="healthcarestorageassista_STORAGE"
)
# 1. Eliminamos el parámetro 'name' de aquí
def blob_trigger_healthcare(myblob: func.InputStream): 
    inicio = time.time()
    
    # 2. Accedemos al nombre a través del objeto myblob
    blob_name = myblob.name 
    
    logging.info("=== [BLOB TRIGGER HEALTHCARE] INICIADO ===")
    logging.info(f"📄 Archivo detectado: {blob_name} | Tamaño: {myblob.length} bytes")

    try:
        # Variables de entorno necesarias
        search_service_name = os.environ["HC_SEARCH_SERVICE_NAME"]
        search_api_key = os.environ["HC_SEARCH_API_KEY"]
        search_indexer_name = os.environ["HC_SEARCH_INDEXER_NAME"]

        # URL del indexador
        url = f"https://{search_service_name}.search.windows.net/indexers/{search_indexer_name}/run?api-version=2024-05-01-preview"
        headers = {
            "Content-Type": "application/json",
            "api-key": search_api_key
        }

        # Llamada al indexador
        response = requests.post(url, headers=headers)
        
        if response.status_code == 202:
            logging.info(f"✅ Indexador ejecutado correctamente: {search_indexer_name}")
        else:
            logging.error(f"⚠️ Error al ejecutar indexador: {response.text}")

    except KeyError as e:
        logging.error(f"❌ Falta variable de entorno: {e}")

    except Exception as e:
        logging.error(f"❌ Error inesperado en blob trigger: {e}")

    duracion = time.time() - inicio
    logging.info(f"=== [FINALIZADO] Tiempo: {duracion:.2f}s ===")