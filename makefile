start-superlinked-server:
	uv run python -m superlinked.server

load-data:
	@echo "📥 Loading procurement data from CSV..."
	curl -X 'POST' \
	'http://localhost:8080/data-loader/product_schema/run' \
	-H 'accept: application/json' \
	-d ''

test-search:
	@echo "🔍 Testing procurement search..."
	curl -X 'POST' \
	'http://localhost:8080/api/v1/search/procurement_query' \
	-H 'accept: application/json' \
	-H 'Content-Type: application/json' \
	-d '{"natural_query": "products with cost less than 5 dollars", "limit": 5}' \
	| jq '.'

test-search-qdrant:
	@echo "🔍 Testing procurement search with Qdrant..."
	curl -X 'POST' \
	'http://localhost:8080/api/v1/search/procurement_query' \
	-H 'accept: application/json' \
	-H 'Content-Type: application/json' \
	-d '{"natural_query": "Show me products that are popular and have a good profit margin", "limit": 5}' \
	| jq '.'

test-category-search:
	@echo "🔍 Testing procurement search with Qdrant..."
	curl -X 'POST' \
	'http://localhost:8080/api/v1/search/procurement_query' \
	-H 'accept: application/json' \
	-H 'Content-Type: application/json' \
	-d '{"natural_query": "low revenue products", "limit": 5}' \
	| jq '.'

test-filter-search:
	@echo "🔍 Testing procurement search with Qdrant..."
	curl -X 'POST' \
	'http://localhost:8080/api/v1/search/procurement_query' \
	-H 'accept: application/json' \
	-H 'Content-Type: application/json' \
	-d '{"natural_query": "Show me products with cost less than 100 dollars and revenue more than 1000 dollars", "limit": 5}' \
	| jq '.'

test-semantic-search:
	@echo "🔍 Testing procurement search with Qdrant..."
	curl -X 'POST' \
	'http://localhost:8080/api/v1/search/procurement_query' \
	-H 'accept: application/json' \
	-H 'Content-Type: application/json' \
	-d '{"natural_query": "Show me products with low revenue and high return rate", "limit": 5}' \
	| jq '.'