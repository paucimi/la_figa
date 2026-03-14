# LA FIGA 🌸
### Plataforma Editorial Inteligente · Revista Digital & Cultural

> *"La expresión natural del cuerpo femenino."*  
> Vol. 1 | 2026

---

## ¿Qué es La Figa?

La Figa es una plataforma editorial basada en agentes de inteligencia artificial diseñada para una revista digital sobre sexualidad desde la perspectiva femenina. El sistema automatiza y potencia las tareas editoriales y de distribución de contenido: desde la investigación de tendencias hasta la publicación en redes sociales, pasando por la generación de artículos y la atención a lectoras y lectores.

El proyecto combina múltiples tecnologías de IA para crear un pipeline editorial completo, educativo, inclusivo y libre de tabúes innecesarios.

---

## Arquitectura del sistema

```
Tema editorial
      │
      ▼
┌─────────────┐
│ Trend Scout │  → Analiza tendencias y ángulos editoriales
└──────┬──────┘
       │
       ▼
┌────────────────┐
│ Content Writer │  → Genera artículos con estilo La Figa
└───────┬────────┘
        │
   ┌────┴─────┐
   │          │
   ▼          ▼
┌──────────┐  ┌──────────────────┐
│   RAG    │  │ Social Publisher │
│Recommender│  │ Instagram/X/TikTok│
└──────────┘  └──────────────────┘

+ Reader Chatbot (agente independiente para lectoras/es)
```

---

## Stack tecnológico

| Tecnología | Uso en el proyecto | Estado |
|---|---|---|
| **Google ADK** | Orquestación multi-agente (SequentialAgent + ParallelAgent) | ✅ Implementado |
| **Google Gemini 2.5 Flash** | Modelo base de todos los agentes | ✅ Implementado |
| **LangChain** | Cadenas de procesamiento y prompts | ✅ Implementado |
| **ChromaDB** | Base de datos vectorial para RAG | ✅ Implementado |
| **Gemini Embeddings** | `text-embedding-004` para indexar artículos | ✅ Implementado |
| **MCP** | Gestión de contexto entre agentes | 🔄 En desarrollo |
| **Streamlit** | Interfaz visual | 🔄 En desarrollo |

---

## Agentes

### 1. Trend Scout
Investiga tendencias editoriales actuales sobre el tema recibido. Identifica ángulos, preguntas frecuentes y mitos persistentes usando búsqueda web.

### 2. Content Writer
Redacta artículos completos con el tono característico de La Figa: educativo, cercano, sin moralismo y con perspectiva femenina.

### 3. RAG Recommender
Recupera artículos del archivo de la revista usando embeddings y búsqueda semántica con ChromaDB. Sugiere contenido relacionado para cada nueva pieza.

### 4. Reader Chatbot
Agente conversacional para lectoras y lectores. Responde preguntas sobre sexualidad de forma cálida, directa y sin juicios.

### 5. Social Publisher
Adapta el contenido editorial a formatos optimizados para Instagram, Twitter/X y TikTok.

---

## Estado del proyecto

- [x] Estructura base del proyecto
- [x] Agente Trend Scout
- [x] Agente Content Writer
- [x] Agente RAG Recommender
- [x] Sistema de embeddings con ChromaDB
- [x] Orquestador ADK (SequentialAgent + ParallelAgent)
- [ ] Agente Reader Chatbot
- [ ] Agente Social Publisher
- [ ] Integración MCP
- [ ] Datos de ejemplo para RAG
- [ ] Interfaz Streamlit
- [ ] Herramientas compartidas (tools/)

---

## Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/paucimi/la_figa.git
cd la_figa

# 2. Activar entorno virtual
source ~/venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Edita .env con tu GOOGLE_API_KEY
```

---

## Uso

```bash
# Ejecutar el pipeline editorial completo
python main.py pipeline "placer femenino y autoconocimiento"

# Usar el chatbot de lectoras/es
python main.py chatbot "¿cómo puedo comunicar mejor mis deseos?"
```

---

## Estructura del proyecto

```
la_figa/
├── agents/               # Los 5 agentes ADK
├── orchestrator/         # Pipeline multi-agente
├── rag/                  # Sistema RAG con embeddings
├── mcp/                  # Model Context Protocol
├── tools/                # Herramientas compartidas
├── data/                 # Artículos base y ChromaDB
├── ui/                   # Interfaz Streamlit
└── main.py               # Punto de entrada
```

---

## Identidad visual

Logo e identidad visual generados con IA (Nano Banana) a partir de prompt propio.  
Concepto: flor de loto con circuitos integrados — naturaleza femenina potenciada por inteligencia artificial.

---

## Autora

**Paola León** · Google ADK · 2026
