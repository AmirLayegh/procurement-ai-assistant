# superlinked_app/app.py
import superlinked.framework as sl
from loguru import logger
from .schema import product_schema
from .index import procurement_index
from .query import procurement_query
from .configs import settings
import os
# Create REST source for real-time data input
product_source: sl.RestSource = sl.RestSource(product_schema)

# Data loader configuration for CSV
logger.info("Data loader will load data from: %s", settings.data_path)

product_data_loader_parser: sl.DataFrameParser = sl.DataFrameParser(
    schema=product_schema,
    mapping={product_schema.product_id: "product_id"}
)

product_data_loader_config: sl.DataLoaderConfig = sl.DataLoaderConfig(
    str(settings.data_path),
    sl.DataFormat.CSV,
    pandas_read_kwargs={"chunksize": settings.chunk_size},
)

product_loader_source: sl.DataLoaderSource = sl.DataLoaderSource(
    product_schema,
    data_loader_config=product_data_loader_config,
    parser=product_data_loader_parser,
)

# Vector database configuration
if settings.use_qdrant_vector_db:
    logger.info("Using Qdrant vector database")
    vector_database = sl.QdrantVectorDatabase(
        settings.qdrant_url.get_secret_value(),
        settings.qdrant_api_key.get_secret_value(),
        collection_name='procurement_products',
    )
else:
    logger.info("Using in-memory database")
    vector_database = sl.InMemoryVectorDatabase()

# Create and register executor
executor = sl.RestExecutor(
    sources=[product_source, product_loader_source],
    indices=[procurement_index],
    queries=[
        sl.RestQuery(sl.RestDescriptor("procurement_query"), procurement_query),
    ],
    vector_database=vector_database,
)

# Register with SuperlinkedRegistry
sl.SuperlinkedRegistry.register(executor)

logger.info("✅ Procurement server registered and ready")