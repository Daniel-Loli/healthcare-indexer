# 📑 HealthCare RAG - Indexer Trigger (Azure Function)

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Azure Functions](https://img.shields.io/badge/Azure_Functions-Serverless-0062AD?logo=azurefunctions)
![Azure Blob Storage](https://img.shields.io/badge/Trigger-Blob_Storage-0078D4?logo=microsoftazure)

Este repositorio contiene una **Azure Function (Python)** diseñada para automatizar la ingestión de datos en tiempo real. Actúa como un disparador que sincroniza la subida de documentos en **Blob Storage** con la ejecución inmediata de los indexadores de **Azure AI Search**.

## ⚙️ Flujo de Trabajo (Event-Driven)

Esta función implementa un patrón de arquitectura reactiva para asegurar que el conocimiento del Chatbot esté siempre actualizado:

1.  **Detección (Blob Trigger):** La función se despierta automáticamente cuando un nuevo archivo (PDF, DOCX) se sube al contenedor configurado (por defecto `docs`).
2.  **Orquestación:** En lugar de procesar el archivo localmente (lo cual sería lento y costoso), la función actúa como controlador.
3.  **Ejecución Remota:** Envía una solicitud HTTP (`POST`) a la API REST de **Azure AI Search** para forzar la ejecución del *Indexer*.
4.  **Indexación:** El servicio de Azure AI Search se encarga de descargar el archivo, aplicar las habilidades cognitivas (OCR, Chunking, Embeddings) y actualizar el índice vectorial.

## 🛠️ Stack Tecnológico

* **Plataforma:** Azure Functions (Python Programming Model V2)
* **Trigger:** Azure Blob Storage Trigger
* **Cliente HTTP:** Python `requests`
* **Destino:** Azure AI Search Management API

## 📂 Estructura del Proyecto

```text
healthcare-indexer/
├── function_app.py        # Código principal: Trigger y lógica de llamada API
├── host.json              # Configuración del runtime de Azure Functions
├── requirements.txt       # Dependencias (azure-functions, requests)
├── local.settings.json    # Variables de entorno locales
└── .gitignore             # Exclusiones de Git
