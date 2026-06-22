import os
import shutil
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter  # Requisito de la rúbrica

def procesar_manual():
    pdf_path = "manual_primeros_auxilios.pdf"
    
    # Limpieza preventiva del almacenamiento local
    if os.path.exists("./chroma_db"):
        print("Borrando carpeta chroma_db antigua...")
        shutil.rmtree("./chroma_db")
    
    print(" 1. Cargando el manual de primeros auxilios (Formatos y Metadatos)...")
    loader = PyMuPDFLoader(pdf_path)
    documentos = loader.load()
    
    print(" 2. Creando fragmentos (chunks) técnicos para optimizar la ventana de contexto...")
    # Configuración ideal para formato diapositiva/manual técnico
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=150)
    chunks = text_splitter.split_documents(documentos)
    
    print(f" 3. Indexando {len(chunks)} fragmentos en el motor local...")
    print(" 4. Generando embeddings semánticos en ESPAÑOL con L12...")
    # Estandarizamos el modelo multilingüe de alta densidad para evitar el desajuste de dimensiones
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    
    vector_store = Chroma.from_documents(
        documents=chunks, 
        embedding=embeddings, 
        persist_directory="./chroma_db"
    )
    
    print("¡Éxito! Nueva base de datos 'chroma_db' guardada físicamente con chunks estructurados.")

if __name__ == "__main__":
    procesar_manual()