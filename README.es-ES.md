

# 🛒 Asistente de IA para Compras

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Google Cloud](https://img.shields.io/badge/Google%20Cloud-Run-4285F4?logo=google-cloud)](https://cloud.google.com/run)
[![Superlinked](https://img.shields.io/badge/Powered%20by-Superlinked-FF6B6B)](https://superlinked.com)

> **🏆 Ganador del Hackathon Firebase Studio Enterprise Vibe Coding 2025**  
> *Parte del lanzamiento de la región de Suecia de Google Cloud*  
> Potenciar a los compradores minoristas con búsqueda semántica impulsada por IA para tomar decisiones de compras inteligentes.

## 🎯 Descripción general

El Asistente de IA para Compras transforma la forma en que los compradores minoristas toman decisiones de compra al proporcionar información inteligente e instantánea a través de búsqueda en lenguaje natural. En lugar de esperar días a que los equipos de ingeniería proporcionen datos, los compradores ahora pueden hacer preguntas como *"Muéstrame vestidos sostenibles por menos de $50 con proveedores confiables"* y obtener resultados prácticos en segundos.

### ✨ Características principales

- 🗣️ **Búsqueda en lenguaje natural** - Consulta usando inglés llano
- ⚡ **Resultados instantáneos** - Tiempos de respuesta de menos de 3 segundos
- 📊 **Análisis inteligentes** - Fiabilidad del proveedor, márgenes de beneficio, tasas de devolución
- 🎯 **Doble propósito** - Sirve tanto a los equipos de compras como de marketing
- 🔍 **Búsqueda vectorial** - Impulsada por una comprensión semántica avanzada



## 🏗️ Arquitectura

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API    │    │  Vector DB      │
│   (Firebase/    │    │                  │    │                 │
     Streamlit)   │◄──►│   (Cloud Run)    │◄──►│    (Qdrant)     │
│                 │    │   Superlinked    │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### Stack tecnológico

- **Backend**: Python 3.11, Framework Superlinked, FastAPI
- **Frontend**: Next.js + TypeScript (Producción) | Streamlit (Desarrollo local)
- **IA/ML**: OpenAI GPT-4, Sentence Transformers, Búsqueda vectorial
- **Base de datos**: Base de datos vectorial Qdrant
- **Infraestructura**: Google Cloud Run, Firebase Hosting
- **Datos**: Catálogo de productos con métricas enriquecidas de proveedores (conjunto de datos de Google Analytics 4 BigQuery)

## 📋 Requisitos previos

- Python 3.11+
- Node.js 18+ (para el frontend de producción)
- Streamlit (para desarrollo local)
- Cuenta de Google Cloud Platform
- Clave API de OpenAI
- Cuenta de Qdrant Cloud (opcional, usa memoria por defecto)

## 🛠️ Instalación

### Configuración del Backend

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/yourusername/procurement-ai-assistant.git
   cd procurement-ai-assistant
   ```

2. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   # o con uv (recomendado)
   uv sync
   ```

3. **Configurar variables de entorno**
   ```bash
   cp .env.example .env
   # Edita .env con tus claves API y configuración
   ```

4. **Iniciar el servidor**
   ```bash
   # Desarrollo
   make start-superlinked-server
   
   # O directamente
   uv run python -m superlinked.server
   ```

### Inicio rápido con Streamlit (Desarrollo local)

Para desarrollo y pruebas locales rápidos:

1. **Iniciar el backend** (sigue los pasos 1-4 anteriores)

2. **Ejecutar el frontend de Streamlit**
   ```bash
   streamlit run st_app/app.py
   ```

3. **Acceder a la aplicación**
   - Interfaz de Streamlit: `http://localhost:8501`
   - API del backend: `http://localhost:8080`

### Configuración del Frontend de Producción (Next.js)

1. **Navegar al directorio del frontend**
   ```bash
   cd frontend
   ```

2. **Instalar dependencias**
   ```bash
   npm install
   ```

3. **Configurar el entorno**
   ```bash
   cp .env.local.example .env.local
   # Agrega el punto de conexión de tu API backend
   ```

4. **Iniciar el servidor de desarrollo**
   ```bash
   npm run dev
   ```

## 🚀 Despliegue

### Desplegar el Backend en Google Cloud Run

1. **Habilitar las API necesarias**
   ```bash
   gcloud services enable run.googleapis.com cloudbuild.googleapis.com
   ```

2. **Desplegar usando el script proporcionado**
   ```bash
   chmod +x deploy.sh
   ./deploy.sh
   ```

   O manualmente:
   ```bash
   gcloud run deploy procurement-api \
     --source . \
     --platform managed \
     --region europe-north2 \
     --allow-unauthenticated \
     --memory 8Gi \
     --cpu 4 \
     --set-env-vars="ENVIRONMENT=production"
   ```

### Desplegar el Frontend en Firebase

1. **Instalar Firebase CLI**
   ```bash
   npm install -g firebase-tools
   ```

2. **Inicializar y desplegar**
   ```bash
   firebase init hosting
   npm run build
   firebase deploy
   ```

## 📊 Ejemplos de uso

### Consultas básicas de búsqueda

```bash
# Cost-optimized products
curl -X POST "https://your-api-url/api/v1/search/procurement_query" \
  -H "Content-Type: application/json" \
  -d '{"natural_query": "products with cost less than 5 dollars", "limit": 5}'

# High-margin, reliable suppliers
curl -X POST "https://your-api-url/api/v1/search/procurement_query" \
  -H "Content-Type: application/json" \
  -d '{"natural_query": "dresses with low cost and high revenue", "limit": 10}'
```

## 🔧 Configuración

### Variables de entorno

| Variable | Descripción | Predeterminado |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Clave API de OpenAI para procesamiento de lenguaje natural | Requerido |
| `QDRANT_URL` | URL de la base de datos vectorial Qdrant | `localhost:6333` |
| `QDRANT_API_KEY` | Clave API de Qdrant | Opcional |
| `DATA_PATH` | Ruta a los datos CSV de productos | `./data/csv/products_enriched.csv` |
| `USE_QDRANT_VECTOR_DB` | Usar Qdrant en lugar de base de datos en memoria | `false` |
| `CHUNK_SIZE` | Tamaño de los bloques para el procesamiento de datos | `10` |

### Esquema de datos

El sistema espera datos CSV con las siguientes columnas:

```csv
product_id,name,category,brand,department,cost,retail_price,profit_margin_percent,
total_orders,return_rate_percent,supplier_reliability_score,avg_sale_price,
total_revenue,daily_sales_rate,days_since_creation,total_items_sold
```

## 🧪 Pruebas

### Pruebas del Backend

```bash
# Load test data
make load-data

# Test basic search
make test-search

# Test category-specific search
make test-category-search
```

### Desarrollo con Streamlit

```bash
# Quick test with Streamlit interface
streamlit run streamlit_app.py
```



## 🤝 Contribuir

1. Bifurca (fork) el repositorio
2. Crea una rama de funcionalidad 
3. Realiza commit de tus cambios 
4. Sube (push) a la rama
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - consulta el archivo [LICENSE](LICENSE) para más detalles.

## 🙏 Agradecimientos

- **Superlinked** por el framework de búsqueda semántica
- **Google Cloud** por la infraestructura de alojamiento
- **Codento** por organizar el hackathon



---

**Construido con ❤️ por Amir**

*Transforma tu proceso de compras de reactivo a predictivo con inteligencia impulsada por IA.*
