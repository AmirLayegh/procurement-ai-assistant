# 🛒 Procurement AI Assistant

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Google Cloud](https://img.shields.io/badge/Google%20Cloud-Run-4285F4?logo=google-cloud)](https://cloud.google.com/run)
[![Superlinked](https://img.shields.io/badge/Powered%20by-Superlinked-FF6B6B)](https://superlinked.com)

> **🏆 Firebase Studio Enterprise Vibe Coding Hackathon Winner 2025**  
> *Part of Google Cloud Sweden Region Launch*  
> Empowering retail buyers with AI-powered semantic search for intelligent procurement decisions.

## 🎯 Overview

Procurement AI Assistant transforms how retail buyers make purchasing decisions by providing instant, intelligent insights through natural language search. Instead of waiting days for engineering teams to provide data, buyers can now ask questions like *"Show me sustainable dresses under $50 with reliable suppliers"* and get actionable results in seconds.

### ✨ Key Features

- 🗣️ **Natural Language Search** - Query using plain English
- ⚡ **Instant Results** - Sub-3-second response times
- 📊 **Smart Analytics** - Supplier reliability, profit margins, return rates
- 🎯 **Dual Purpose** - Serves both procurement and marketing teams
- 🔍 **Vector Search** - Powered by advanced semantic understanding



## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API    │    │  Vector DB      │
│   (Firebase/    │    │                  │    │                 │
     Streamlit)   │◄──►│   (Cloud Run)    │◄──►│    (Qdrant)     │
│                 │    │   Superlinked    │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### Tech Stack

- **Backend**: Python 3.11, Superlinked Framework, FastAPI
- **Frontend**: Next.js + TypeScript (Production) | Streamlit (Local Development)
- **AI/ML**: OpenAI GPT-4, Sentence Transformers, Vector Search
- **Database**: Qdrant Vector Database
- **Infrastructure**: Google Cloud Run, Firebase Hosting
- **Data**: Product catalog with enriched supplier metrics (Google Analytics 4 BigQuery dataset)

## 📋 Prerequisites

- Python 3.11+
- Node.js 18+ (for production frontend)
- Streamlit (for local development)
- Google Cloud Platform account
- OpenAI API key
- Qdrant Cloud account (optional, uses in-memory by default)

## 🛠️ Installation

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/procurement-ai-assistant.git
   cd procurement-ai-assistant
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   # or with uv (recommended)
   uv sync
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

4. **Start the server**
   ```bash
   # Development
   make start-superlinked-server
   
   # Or directly
   uv run python -m superlinked.server
   ```

### Quick Start with Streamlit (Local Development)

For rapid local development and testing:

1. **Start the backend** (follow steps 1-4 above)

2. **Run Streamlit frontend**
   ```bash
   streamlit run st_app/app.py
   ```

3. **Access the app**
   - Streamlit UI: `http://localhost:8501`
   - Backend API: `http://localhost:8080`

### Production Frontend Setup (Next.js)

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Configure environment**
   ```bash
   cp .env.local.example .env.local
   # Add your backend API endpoint
   ```

4. **Start development server**
   ```bash
   npm run dev
   ```

## 🚀 Deployment

### Deploy Backend to Google Cloud Run

1. **Enable required APIs**
   ```bash
   gcloud services enable run.googleapis.com cloudbuild.googleapis.com
   ```

2. **Deploy using the provided script**
   ```bash
   chmod +x deploy.sh
   ./deploy.sh
   ```

   Or manually:
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

### Deploy Frontend to Firebase

1. **Install Firebase CLI**
   ```bash
   npm install -g firebase-tools
   ```

2. **Initialize and deploy**
   ```bash
   firebase init hosting
   npm run build
   firebase deploy
   ```

## 📊 Usage Examples

### Basic Search Queries

```bash
# Cost-optimized products
curl -X POST "https://your-api-url/api/v1/search/procurement_query" \
  -H "Content-Type: application/json" \
  -d '{"natural_query": "products with cost less than 5 dollars", "limit": 5}'

# High-margin, reliable suppliers
curl -X POST "https://your-api-url/api/v1/search/procurement_query" \
  -H "Content-Type: application/json" \
  -d '{"natural_query": "dresses with high profit margin from reliable suppliers", "limit": 10}'
```

### Frontend Usage

```typescript
// Search with natural language
const searchProducts = async (query: string) => {
  const response = await fetch('/api/v1/search/procurement_query', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ natural_query: query, limit: 20 })
  });
  return response.json();
};
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key for natural language processing | Required |
| `QDRANT_URL` | Qdrant vector database URL | `localhost:6333` |
| `QDRANT_API_KEY` | Qdrant API key | Optional |
| `DATA_PATH` | Path to product CSV data | `./data/csv/products_enriched.csv` |
| `USE_QDRANT_VECTOR_DB` | Use Qdrant vs in-memory database | `false` |
| `CHUNK_SIZE` | Data processing chunk size | `10` |

### Data Schema

The system expects CSV data with the following columns:

```csv
product_id,name,category,brand,department,cost,retail_price,profit_margin_percent,
total_orders,return_rate_percent,supplier_reliability_score,avg_sale_price,
total_revenue,daily_sales_rate,days_since_creation,total_items_sold
```

## 🧪 Testing

### Backend Tests

```bash
# Load test data
make load-data

# Test basic search
make test-search

# Test category-specific search
make test-category-search
```

### Streamlit Development

```bash
# Quick test with Streamlit interface
streamlit run streamlit_app.py
```



## 🤝 Contributing

1. Fork the repository
2. Create a feature branch 
3. Commit your changes 
4. Push to the branch
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Superlinked** for the semantic search framework
- **Google Cloud** for hosting infrastructure
- **Codento** for organizing the hackathon





---

**Built with ❤️ for retail professionals who deserve better procurement tools.**

*Transform your procurement process from reactive to predictive with AI-powered intelligence.*