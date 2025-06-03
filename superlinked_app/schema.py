# procurement/schema.py
from superlinked import framework as sl

class ProductSchema(sl.Schema):
    product_id: sl.IdField
    
    # Text fields for embedding
    name: sl.String
    category: sl.String
    brand: sl.String
    department: sl.String
    
    # Numeric optimization fields
    cost: sl.Float
    retail_price: sl.Float
    profit_margin_percent: sl.Float
    
    # Performance metrics
    total_orders: sl.Integer
    return_rate_percent: sl.Float
    supplier_reliability_score: sl.Float
    avg_sale_price: sl.Float
    
    # Additional metrics
    total_revenue: sl.Float
    daily_sales_rate: sl.Float
    days_since_creation: sl.Integer
    total_items_sold: sl.Integer

# Create schema instance
product_schema = ProductSchema()