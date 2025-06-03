# procurement/index.py
from superlinked import framework as sl
from superlinked_app.schema import product_schema

# Text similarity spaces for product search
product_text_space = sl.TextSimilaritySpace(
    text=[
        product_schema.name, 
        # product_schema.category, 
        # product_schema.brand
    ],
    model="sentence-transformers/all-MiniLM-L12-v2"
)

# product_brand_space = sl.TextSimilaritySpace(
#     text=[
#         product_schema.brand,
#     ],
#     model="sentence-transformers/all-MiniLM-L12-v2"
# )

# product_category_space = sl.CategoricalSimilaritySpace(
#     category_input=product_schema.category,
#     categories=[
#         "Accessories", "Plus", "Swim", "Active", "Socks & Hosiery", "Socks", "Dresses",
#         "Pants & Capris", "Fashion Hoodies & Sweatshirts", "Skirts", "Blazers & Jackets", "Suits",
#         "Tops & Tees", "Sweaters", "Shorts", "Jeans", "Maternity", "Sleep & Lounge", "Suits & Sport Coats",
#         "Pants", "Intimates", "Outerwear & Coats", "Underwear", "Leggings", "Jumpsuits & Rompers", "Clothing Sets"
#     ],
#     uncategorized_as_category=True,
#     negative_filter=-1
# )

# Cost optimization (lower is better for procurement)
cost_space = sl.NumberSpace(
    product_schema.cost,
    min_value=0,
    max_value=500.0,
    mode=sl.Mode.MINIMUM,  # Lower cost preferred
    scale=sl.LogarithmicScale(),
)

# Profit margin optimization (higher is better)
profit_margin_space = sl.NumberSpace(
    product_schema.profit_margin_percent,
    min_value=0.0,
    max_value=100.0,
    mode=sl.Mode.MAXIMUM,
    scale=sl.LogarithmicScale()
)

# Supplier reliability (higher is better)
reliability_space = sl.NumberSpace(
    product_schema.supplier_reliability_score,
    min_value=0.0,
    max_value=10.0,
    mode=sl.Mode.MAXIMUM,
)

# Return rate optimization (lower is better)
return_rate_space = sl.NumberSpace(
    product_schema.return_rate_percent,
    min_value=0.0,
    max_value=100.0,
    mode=sl.Mode.MINIMUM,  # Lower return rate preferred
)

# Sales performance (higher is better)
sales_volume_space = sl.NumberSpace(
    product_schema.total_orders,
    min_value=0,
    max_value=1000,
    mode=sl.Mode.MAXIMUM,
    scale=sl.LogarithmicScale()
)

# Revenue performance (higher is better)
revenue_space = sl.NumberSpace(
    product_schema.total_revenue,
    min_value=0,
    max_value=50000,
    mode=sl.Mode.MAXIMUM,
    scale=sl.LogarithmicScale()
)

# Create the procurement index
procurement_index = sl.Index(
    spaces=[
        product_text_space,
        #product_brand_space,
        #product_category_space,
        cost_space,
        profit_margin_space,
        reliability_space,
        return_rate_space,
        sales_volume_space,
        revenue_space,
    ],
    fields=[
        product_schema.department,
        product_schema.category,
        product_schema.brand,
        product_schema.cost,
        product_schema.retail_price,
        product_schema.profit_margin_percent,
        product_schema.return_rate_percent,
        product_schema.total_orders,
        product_schema.total_revenue,
        product_schema.supplier_reliability_score,
        product_schema.avg_sale_price,
        product_schema.days_since_creation,
    ]
)