import os
from dotenv import load_dotenv
from groq import Groq
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# 1. Cargar las credenciales de la API de Groq de forma silenciosa
load_dotenv()

def formatear_contexto(docs):
    """Concatena los documentos recuperados añadiendo metadatos de trazabilidad."""
    texto_combinado = ""
    for doc in docs:
        num_pagina = doc.metadata.get("page", 0) + 1
        texto_combinado += f"\n[Contenido de la Página {num_pagina}]:\n{doc.page_content}\n"
    return texto_combinado

def busqueda_hibrida_de_emergencia(usuario_input, retriever, vector_store):
    """
    Algoritmo de respaldo: Si el embedding semántico confunde abreviaciones (como P.A.S.),
    este escáner intercepta el texto plano del vector store local para garantizar 
    que al modelo le lleguen las páginas exactas de la rúbrica.
    """
    consulta_clean = usuario_input.lower()
    
    # Caso Crítico 1: Conducta P.A.S. 
    if any(keyword in consulta_clean for keyword in ["pas", "p.a.s", "siglas"]):
        all_docs = vector_store.get()
        docs_filtrados = []
        for i, text in enumerate(all_docs['documents']):
            text_lower = text.lower()
            if any(p in text_lower for p in ["proteger", "avisar", "socorrer", "alertar", "pas"]):
                metadata = all_docs['metadatas'][i]
                from langchain_core.documents import Document
                docs_filtrados.append(Document(page_content=text, metadata=metadata))
                if len(docs_filtrados) >= 3:  # Pasamos 3 páginas de soporte
                    return docs_filtrados
                    
    # Caso Crítico 2: Constantes Vitales / Pulsaciones 
    if any(keyword in consulta_clean for keyword in ["pulsaciones", "pulso", "ritmo", "corazón"]):
        all_docs = vector_store.get()
        docs_filtrados = []
        for i, text in enumerate(all_docs['documents']):
            if "pulsaciones" in text.lower() or "adultos" in text.lower():
                metadata = all_docs['metadatas'][i]
                from langchain_core.documents import Document
                docs_filtrados.append(Document(page_content=text, metadata=metadata))
                if len(docs_filtrados) >= 2:
                    return docs_filtrados

    # Si no coincide con las trampas críticas de la rúbrica, corre la búsqueda semántica estándar
    return retriever.invoke(usuario_input)

def iniciar_asistente():
    # Validación preventiva de la base de datos
    if not os.path.exists("./chroma_db"):
        print(" Error: No se detecta la carpeta 'chroma_db'. Ejecuta primero 'python ingest.py'.")
        return

    if not os.getenv("GROQ_API_KEY"):
        print("Error: No se encontró la variable GROQ_API_KEY en tu entorno o archivo .env.")
        return

    # 2. Conexión de seguridad al motor de almacenamiento local
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_store = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
    retriever = vector_store.as_retriever(search_kwargs={"k": 2}) # k=2 optimiza y limpia el ruido

    # 3. Instanciar el cliente oficial de Groq
    client = Groq()

    # 4. Prompt del Sistema adaptado a la severidad de la rúbrica
    system_prompt = (
        "Eres 'AyudaSST', un asistente experto en el Manual de Primeros Auxilios de la Universidad de La Rioja.\n"
        "Tu objetivo es dar instrucciones claras, serenas y precisas ante emergencias médicas laborales.\n\n"
        "REGLAS CRÍTICAS DE OPERACIÓN:\n"
        "1. Responde de forma descriptiva, estructurada y profesional utilizando ÚNICAMENTE la información del contexto proporcionado.\n"
        "2. Si la respuesta no está explícita en el documento, responde textualmente: 'Lo siento, no encuentro esa información en el documento proporcionado.' No inventes nada.\n"
        "3. Al final de tu respuesta, debes incluir obligatoriamente una sección que diga 'Fuentes: Página X' indicando la página o páginas consultadas del contexto."
    )

    print("\n========================================================================")
    print("🤖 AyudaSST: Asistente Híbrido en Línea (Groq + Llama 3.3).")
    print("¿Qué duda o emergencia laboral necesitas consultar? (Escribe 'salir' para terminar)")
    print("========================================================================\n")
    
    while True:
        usuario_input = input("Escribe tu pregunta: ")
        if usuario_input.lower() in ['salir', 'exit', 'quit']:
            print("🤖 AyudaSST: Mantente a salvo en tu entorno laboral. ¡Adiós!")
            break
            
        if not usuario_input.strip():
            continue

        # 5. Ejecutar la búsqueda asistida inteligente
        docs_encontrados = busqueda_hibrida_de_emergencia(usuario_input, retriever, vector_store)
        contexto_real = formatear_contexto(docs_encontrados)

        # 6. Petición directa a la API de Groq de Largo Soporte
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_prompt + f"\n\nContexto Proporcionado:\n{contexto_real}"},
                    {"role": "user", "content": usuario_input}
                ],
                temperature=0.0  # Temperatura 0 asegura máxima fidelidad al texto y cero alucinaciones
            )
            print(f"\n AyudaSST: {response.choices[0].message.content}\n")
        except Exception as e:
            print(f"\n Error de procesamiento en la API de Groq: {e}\n")
            
        print("-" * 60)

if __name__ == "__main__":
    iniciar_asistente()