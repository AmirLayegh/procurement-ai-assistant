"""
Pytest configuration and fixtures for the procurement AI assistant tests.
"""
import os
import pytest
from unittest.mock import MagicMock, patch
from pydantic import SecretStr
import pandas as pd


@pytest.fixture
def mock_settings():
    """Mock settings for testing without real API keys."""
    # Import here to avoid app initialization during collection
    from superlinked_app.configs import Settings
    
    return Settings(
        text_embedder_name="sentence-transformers/all-MiniLM-L6-v2",
        chunk_size=5,
        openai_model="gpt-4o",
        openai_api_key=SecretStr("test-openai-key"),
        qdrant_api_key=SecretStr("test-qdrant-key"),
        qdrant_url=SecretStr("http://localhost:6333"),
        qdrant_collection_name=SecretStr("test_collection"),
        data_path="./tests/data/products_enriched.csv",
        use_qdrant_vector_db=False,  # Use in-memory for tests
    )


@pytest.fixture
def sample_product_data():
    """Sample product data for testing."""
    return {
        "product_id": "PROD001",
        "name": "Classic Blue Jeans",
        "category": "Jeans", 
        "brand": "TestBrand",
        "department": "Women",
        "cost": 25.00,
        "retail_price": 89.99,
        "profit_margin_percent": 72.2,
        "total_orders": 150,
        "return_rate_percent": 5.5,
        "supplier_reliability_score": 8.7,
        "avg_sale_price": 79.99,
        "total_revenue": 11998.50,
        "daily_sales_rate": 2.5,
        "days_since_creation": 60,
        "total_items_sold": 150
    }


@pytest.fixture
def sample_product_dataframe():
    """Sample product DataFrame for testing."""
    data = [
        {
            "product_id": "PROD001",
            "name": "Classic Blue Jeans",
            "category": "Jeans",
            "brand": "TestBrand",
            "department": "Women",
            "cost": 25.00,
            "retail_price": 89.99,
            "profit_margin_percent": 72.2,
            "total_orders": 150,
            "return_rate_percent": 5.5,
            "supplier_reliability_score": 8.7,
            "avg_sale_price": 79.99,
            "total_revenue": 11998.50,
            "daily_sales_rate": 2.5,
            "days_since_creation": 60,
            "total_items_sold": 150
        },
        {
            "product_id": "PROD002", 
            "name": "Premium Cotton T-Shirt",
            "category": "Tops & Tees",
            "brand": "PremiumBrand",
            "department": "Men",
            "cost": 15.00,
            "retail_price": 39.99,
            "profit_margin_percent": 62.5,
            "total_orders": 300,
            "return_rate_percent": 2.1,
            "supplier_reliability_score": 9.2,
            "avg_sale_price": 35.99,
            "total_revenue": 10797.00,
            "daily_sales_rate": 5.0,
            "days_since_creation": 30,
            "total_items_sold": 300
        }
    ]
    return pd.DataFrame(data)


@pytest.fixture
def mock_openai_response():
    """Mock OpenAI API response for natural language queries."""
    return {
        "choices": [
            {
                "message": {
                    "content": """
                    {
                        "cost_weight": 8,
                        "reliability_weight": 5,
                        "profit_margin_weight": 3,
                        "return_rate_weight": 0,
                        "sales_performance_weight": 2,
                        "revenue_performance_weight": 1,
                        "description_weight": 1,
                        "product_description": "affordable jeans",
                        "departments_include": ["Women"],
                        "categories_include": ["Jeans"],
                        "min_cost": 0,
                        "max_cost": 50
                    }
                    """
                }
            }
        ]
    }


@pytest.fixture
def mock_qdrant_client():
    """Mock Qdrant client for testing."""
    client = MagicMock()
    client.search.return_value = MagicMock()
    client.create_collection.return_value = True
    client.upsert.return_value = True
    return client


# Patch external dependencies for all tests
@pytest.fixture(autouse=True)
def mock_external_dependencies():
    """Automatically mock external dependencies for all tests."""
    with patch.dict(os.environ, {
        "OPENAI_API_KEY": "test-key",
        "QDRANT_API_KEY": "test-key",
        "QDRANT_URL": "http://localhost:6333"
    }):
        yield


@pytest.fixture
def test_data_dir(tmp_path):
    """Create a temporary directory with test data."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    
    # Create test CSV file with the same name as the real data file
    test_csv = data_dir / "products_enriched.csv"
    sample_data = pd.DataFrame([
        {
            "product_id": "TEST001",
            "name": "Test Product",
            "category": "Test Category",
            "brand": "Test Brand", 
            "department": "Women",
            "cost": 10.0,
            "retail_price": 25.0,
            "profit_margin_percent": 60.0,
            "total_orders": 100,
            "return_rate_percent": 3.0,
            "supplier_reliability_score": 8.5,
            "avg_sale_price": 22.0,
            "total_revenue": 2200.0,
            "daily_sales_rate": 1.0,
            "days_since_creation": 45,
            "total_items_sold": 100
        }
    ])
    sample_data.to_csv(test_csv, index=False)
    
    return data_dir


@pytest.fixture
def natural_query_examples():
    """Sample natural language queries for testing."""
    return [
        "cheap products under 20 dollars",
        "high margin dresses from reliable suppliers",
        "best selling items in men's category",
        "sustainable clothing with low return rates",
        "premium brands with excellent profit margins"
    ]


@pytest.fixture
def product_schema():
    """Product schema fixture for testing."""
    # Import here to avoid initialization during collection
    from superlinked_app.schema import product_schema
    return product_schema 