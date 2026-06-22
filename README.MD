# Sistema RAG - Asistente de Primeros Auxilios (AyudaSST)

**Estudiante:** [SARA VALENTINA MENDIETA BOHORQUEZ]  
**Fecha:** Junio 2026  

---

## 1. Documento Seleccionado y Justificación
* **Documento:** Manual de Primeros Auxilios - Servicio de Prevención de Riesgos Laborales (Universidad de La Rioja).
* **Justificación:** Se seleccionó este documento de 205 páginas debido a su naturaleza crítica. En entornos laborales, consultar rápidamente protocolos de emergencia como la maniobra de Heimlich, RCP o el control de hemorragias puede marcar la diferencia. El sistema RAG permite extraer instrucciones precisas y trazables sin necesidad de navegar manualmente por extensas diapositivas en un momento de tensión.

## 2. Persona Usuaria Objetivo y Caso de Uso

### Persona Usuaria Objetivo
* **Delegados de prevención y brigadistas de emergencias** en centros de trabajo.
* **Integrantes del Comité de Seguridad y Salud en el Trabajo (SST)**.
* **Personal de oficinas o laboratorios** que requiera actuar como primer eslabón en la cadena de supervivencia ante un incidente.

### Caso de Uso General
Durante la jornada laboral, ocurre un accidente imprevisto en las instalaciones de la empresa (por ejemplo: un colapso por lipotimia, una caída que resulta en fractura abierta, un atragantamiento en el área de cafetería o una parada cardiorrespiratoria). 

Ante la situación de alta tensión, el brigadista o trabajador a cargo no dispone del tiempo para buscar en un manual extenso de más de 100 diapositivas. En su lugar, abre el asistente conversacional **AyudaSST** e introduce preguntas directas en lenguaje natural (ej. *¿Cómo actuar ante una fractura abierta?* o *¿Cuáles son los pasos del sistema P.A.S.?*). El sistema le devuelve en segundos el protocolo médico exacto y estructurado del manual, permitiéndole estabilizar a la víctima de manera serena, precisa y segura mientras los servicios de asistencia profesional (ambulancia) acuden al lugar.

### Preguntas

¿Cuál es la cifra normal de pulsaciones por minuto para un adulto y para un anciano?

Según la información proporcionada en la Página 32, las cifras normales del pulso son:

Para adultos: 72 a 80 pulsaciones por minuto
Para ancianos: 60 o menos pulsaciones por minuto
Fuentes: Página 32



¿Se puede aplicar presión directa en una herida si hay una fractura abierta?

No, no se puede aplicar presión directa en una herida si hay una fractura abierta. Esto se establece explícitamente como una excepción en el protocolo de hemorragias externas.

Fuentes: Página 87, Página 88



¿Cuáles son los tres principios básicos de la actuación general ante una emergencia (Sistema P.A.S.)?

Según el contexto proporcionado, los tres principios básicos de la actuación general ante una emergencia (Sistema P.A.S.) son:

Proteger: Al accidentado, a uno mismo y a los demás.
Alertar: A los servicios de atención sanitaria.
Socorrer: Al accidentado o herido.
Estos principios se mencionan en la página 16 del contexto proporcionado.

Fuentes: Página 16




¿Qué se debe explorar en la evaluación primaria de una víctima y en qué orden?

En la evaluación primaria de una víctima, se deben explorar varios aspectos para determinar el estado de la persona y proporcionar la atención adecuada. Según el contenido de la Página 38, los aspectos a explorar son:

Puntos dolorosos
Heridas y contusiones
Deformidades
Sensibilidad / Movilidad
Cabeza
Cuello
Tórax y abdomen
Extremidades
En cuanto al orden, no se especifica un orden determinado en el contenido proporcionado. Sin embargo, en la evaluación primaria, generalmente se sigue un patrón de evaluación que comienza con la valoración de la conciencia y la respiración, seguida de la evaluación de la circulación y la exploración de lesiones y heridas.

Fuentes: Página 38




¿Cómo se define legalmente un accidente de trabajo en el manual?

Según el manual, se entiende por accidente de trabajo "toda lesión corporal que el trabajador sufra con ocasión o a consecuencia del trabajo que ejecuta por cuenta ajena".

Fuentes: Página 5




¿Cuáles son las medidas de prevención indicadas para evitar infecciones por virus como la Hepatitis B, C o el VIH al auxiliar a un accidentado?

Al auxiliar a un accidentado, es fundamental tomar medidas de prevención para evitar infecciones por virus como la Hepatitis B, C o el VIH. Según el contenido de la Página 15, las medidas de prevención indicadas son:

Utilizar material desechable, de un solo uso.
No compartir material de cura entre dos accidentados.
Evitar el contacto directo con la sangre del accidentado.
Estas medidas ayudan a prevenir las infecciones por virus hepatitis B y C, así como el Virus de la Inmunodeficiencia Humana (VIH).

Fuentes: Página 15




¿Cuáles son los síntomas característicos de un shock y qué postura corporal se debe adoptar si las lesiones lo permiten?

Según el contexto proporcionado, en la página 102 se menciona que en caso de shock, se debe controlar los signos vitales, tratar las lesiones que lo provocan, aflojar todo lo que comprima a la víctima y evitar pérdida de calor corporal. Si las lesiones lo permiten, se debe colocar la cabeza más baja que los pies.

No se mencionan explícitamente los síntomas característicos del shock en el contexto proporcionado, pero se describe la actuación en caso de shock.

La postura corporal recomendada si las lesiones lo permiten es colocar la cabeza más baja que los pies.

Fuentes: Página 102




¿Cuál es la dosis recomendada de Ibuprofeno para un dolor de cabeza adulto?

Lo siento, no encuentro esa información en el documento proporcionado.

Fuentes: Página 204, Página 143, Página 135




¿Quién ganará el próximo mundial de fútbol?

Lo siento, no encuentro esa información en el documento proporcionado.

Fuentes: Página 155, Página 156, Página 125

## Vídeo

https://youtu.be/E0VafR9PbvI 

## 3. Instrucciones de Ejecución

### Requisitos Previos
* **Python:** Versión 3.10 o superior (Desarrollado y probado sobre Python 3.14).
* **Credenciales:** Una cuenta en Groq Cloud para la obtención de una API Key gratuita.

### Configuración del Archivo de Entorno (`.env`)
En la raíz del proyecto, debes crear un archivo oculto llamado exactamente `.env` (asegúrate de que no tenga extensión `.txt`) y añadir tu clave privada de la siguiente manera:
```text
GROQ_API_KEY=gsk_tu_clave_secreta_de_groq_aqui