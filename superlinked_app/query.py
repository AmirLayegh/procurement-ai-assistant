# procurement/query.py
from superlinked import framework as sl
import os
import pandas as pd
from collections import namedtuple
from .schema import product_schema
from .index import (
    procurement_index,
    product_text_space,
    cost_space,
    profit_margin_space,
    reliability_space,
    return_rate_space,
    sales_volume_space,
    revenue_space,
    #product_brand_space,
)
from .nlq import (
    system_prompt,
    cost_description,
    reliability_description,
    profit_margin_description,
    return_rate_description,
    sales_performance_description,
    revenue_performance_description,
    product_description,
    department_description,
    category_description,
    brand_description,
)
from .configs import settings

from dotenv import load_dotenv
load_dotenv(override=True)

# Main procurement query
procurement_query = (
    sl.Query(
        procurement_index,
        weights={
            cost_space: sl.Param(
                "cost_weight",
                description=cost_description,
            ),
            reliability_space: sl.Param(
                "reliability_weight", 
                description=reliability_description,
            ),
            profit_margin_space: sl.Param(
                "profit_margin_weight",
                description=profit_margin_description,
            ),
            return_rate_space: sl.Param(
                "return_rate_weight",
                description=return_rate_description,
            ),
            sales_volume_space: sl.Param(
                "sales_performance_weight",
                description=sales_performance_description,
            ),
            revenue_space: sl.Param(
                "revenue_performance_weight",
                description=revenue_performance_description,
            ),
            product_text_space: sl.Param("description_weight", default=1.0),
        },
    )
    .find(product_schema)
    .similar(
        product_text_space.text,
        sl.Param("product_description", description=product_description),
        weight=sl.Param("similar_description_weight", default=1.0),
    )
)

# Add numerical filters
procurement_query = (
    procurement_query
    .filter(product_schema.cost >= sl.Param("min_cost", default=0))
    .filter(product_schema.cost <= sl.Param("max_cost", default=1000))
    .filter(product_schema.profit_margin_percent >= sl.Param("min_profit_margin", default=0))
    .filter(product_schema.return_rate_percent <= sl.Param("max_return_rate", default=100))
    .filter(product_schema.total_orders >= sl.Param("min_orders", default=0))
    .filter(product_schema.total_revenue >= sl.Param("min_revenue", default=0))
)

# Add categorical filters
procurement_query = procurement_query.filter(
    product_schema.department.in_(
        sl.Param(
            "departments_include",
            description=department_description,
            options=["Women", "Men", "Kids"]
        )
    )
)

CategoryFilter = namedtuple("CategoryFilter", ["operator", "param_name", "category_name", "description", "options"])

filters = [
    CategoryFilter(
        operator=product_schema.category.in_,
        param_name="categories_include",
        category_name="category",
        description="Categories that should be included in search",
        options=["Accessories", "Plus", "Swim", "Active", "Socks & Hosiery", "Socks", "Dresses",
        "Pants & Capris", "Fashion Hoodies & Sweatshirts", "Skirts", "Blazers & Jackets", "Suits",
        "Tops & Tees", "Sweaters", "Shorts", "Jeans", "Maternity", "Sleep & Lounge", "Suits & Sport Coats",
        "Pants", "Intimates", "Outerwear & Coats", "Underwear", "Leggings", "Jumpsuits & Rompers", "Clothing Sets"]
    ),
    CategoryFilter(
        operator=product_schema.category.not_in_,
        param_name="categories_exclude",
        category_name="category",
        description="Categories that should be excluded from search",
        options=["Accessories", "Plus", "Swim", "Active", "Socks & Hosiery", "Socks", "Dresses",
        "Pants & Capris", "Fashion Hoodies & Sweatshirts", "Skirts", "Blazers & Jackets", "Suits",
        "Tops & Tees", "Sweaters", "Shorts", "Jeans", "Maternity", "Sleep & Lounge", "Suits & Sport Coats",
        "Pants", "Intimates", "Outerwear & Coats", "Underwear", "Leggings", "Jumpsuits & Rompers", "Clothing Sets"]
    ),
    CategoryFilter(
        operator=product_schema.brand.in_,
        param_name="brands_include",
        category_name="brand",
        description="Brands that should be included in search",
        options=pd.read_csv('./data/csv/products_enriched.csv')['brand'].unique().tolist()
    )
]

for filter_item in filters:
    param=sl.Param(
        filter_item.param_name,
        description=filter_item.description,
        options=filter_item.options
    )
    procurement_query = procurement_query.filter(filter_item.operator(param))

# Add natural query processing (the key feature!)
procurement_query = procurement_query.with_natural_query(
    natural_query=sl.Param("natural_query"),
    client_config=sl.OpenAIClientConfig(
        api_key=settings.openai_api_key.get_secret_value(), 
        model=settings.openai_model
    ),
    system_prompt=system_prompt
)

# Set result limits and metadata
procurement_query = procurement_query.limit(sl.Param("limit", default=10))
procurement_query = procurement_query.select_all()
procurement_query = procurement_query.include_metadata()