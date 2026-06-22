import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq  # <-- Usamos Groq de forma nativa y estable, debido a problemas con Gemini y OpenAI
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# 1. Configuración de la página web de Streamlit 
st.set_page_config(
    page_title="AyudaSST - Asistente RAG",
    page_icon="🤖",
    layout="centered"
)

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# 2. Inicialización de componentes en caché (Previene recargas lentas en la interfaz)
@st.cache_resource
def inicializar_componentes():
    if not os.path.exists("./chroma_db"):
        return None, None
    
    # Conexión al motor vectorial de embeddings locales
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_store = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
    
    # Configuración del buscador avanzado MMR de amplio espectro (Evita hardcoding)
    retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 4, "fetch_k": 10}
    )
    
    # Instanciar el cliente oficial de Groq DENTRO de la función
    client_groq = Groq()
    
    return retriever, client_groq

def formatear_contexto(docs):
    """Estructura el contexto recuperado manteniendo la trazabilidad por página."""
    texto_combinado = ""
    for doc in docs:
        num_pagina = doc.metadata.get("page", 0) + 1
        texto_combinado += f"\n[Contenido de la Página {num_pagina}]:\n{doc.page_content}\n"
    return texto_combinado

# Carga de recursos globales (Asignamos correctamente las dos variables creadas)
retriever, client = inicializar_componentes()

# Prompt optimizado para modelos analíticos avanzados (Llama 3.3)
SYSTEM_PROMPT = (
    "Eres 'AyudaSST', un asistente virtual experto en el Manual de Primeros Auxilios de la Universidad de La Rioja.\n"
    "Tu objetivo es dar instrucciones claras, serenas, estructuradas y detalladas ante emergencias médicas laborales.\n\n"
    "REGLAS CRÍTICAS DE OPERACIÓN:\n"
    "1. Analiza minuciosamente todo el contexto proporcionado abajo. Si el contexto menciona siglas (como P.A.S.) o protocolos, utiliza el desglose explícito que aparezca en cualquiera de las páginas recuperadas para armar una respuesta completa.\n"
    "2. Responde utilizando ÚNICAMENTE la información del contexto proporcionado. Si la respuesta no se encuentra en el texto bajo ninguna circunstancia, responde textualmente: 'Lo siento, no encuentro esa información en el documento proporcionado.' No inventes nada.\n"
    "3. Al final de tu respuesta, debes listar obligatoriamente las páginas consultadas en una sección llamada 'Fuentes: Página X'."
)

# 3. Estructuración y Diseño Visual de la Aplicación Web
st.title("🤖 AyudaSST")
st.subheader("Asistente experto en Seguridad y Salud en el Trabajo")
st.write("Haz preguntas en lenguaje natural sobre el Manual de Primeros Auxilios.")

# Validación preventiva de la base de datos
if retriever is None or client is None:
    st.error("❌ No se detecta la base de datos 'chroma_db' o la configuración del cliente. Por favor, ejecuta primero 'python ingest.py' en tu terminal.")
    st.stop()

# 4. Gestión de Memoria del Historial del Chat (Session State)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "¡Hola! Soy AyudaSST. ¿Qué duda o emergencia laboral necesitas consultar respecto al manual?"}
    ]

# Dibujar el historial dinámico de la conversación en pantalla
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Intercepción y Procesamiento del Chat en Tiempo Real
if prompt_usuario := st.chat_input("Escribe tu pregunta aquí..."):
    
    # Renderizar inmediatamente la pregunta del usuario en pantalla
    with st.chat_message("user"):
        st.markdown(prompt_usuario)
    st.session_state.messages.append({"role": "user", "content": prompt_usuario})

    # Recuperación semántica RAG mediante MMR
    docs_encontrados = retriever.invoke(prompt_usuario)
    contexto_real = formatear_contexto(docs_encontrados)

    # Bloque de carga asíncrona visual mientras la IA procesa la respuesta
    with st.chat_message("assistant"):
        with st.spinner("Rastreando protocolos en el manual técnico..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT + f"\n\nContexto de Referencia:\n{contexto_real}"},
                        {"role": "user", "content": prompt_usuario}
                    ],
                    temperature=0.0
                )
                respuesta_ia = response.choices[0].message.content
                st.markdown(respuesta_ia)
                
                # Guardar en el historial de sesión
                st.session_state.messages.append({"role": "assistant", "content": respuesta_ia})
                
            except Exception as e:
                st.error(f"Error de procesamiento en la API de Groq: {e}")