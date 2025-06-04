# procurement/nlq.py

# Weight descriptions for natural language processing
cost_description = (
    "Weight for cost optimization. "
    "Higher weight means preference for LOWER cost products. "
    "Keywords indicating cost preference: "
    "Positive: 'cheap', 'affordable', 'budget', 'cost-effective', 'lowest cost', 'economical', 'inexpensive' "
    "Negative: 'expensive', 'premium', 'high-end', 'luxury', 'costly' "
    "Neutral (0): no cost preference mentioned"
)

reliability_description = (
    "Weight for supplier reliability. "
    "Higher weight means preference for MORE reliable suppliers/brands. "
    "Keywords indicating reliability preference: "
    "Positive: 'reliable', 'trustworthy', 'consistent', 'dependable', 'proven', 'established', 'quality' "
    "Negative: 'unreliable', 'inconsistent', 'new', 'untested' "
    "Consider return rates, delivery performance, brand reputation."
)

profit_margin_description = (
    "Weight for profit margin optimization. "
    "Higher weight means preference for products with BETTER margins. "
    "Weight depends on the adjective or noun used to describe the profit margin. "
    "For example: "
    "positive weight: 'profitable', 'high margin', 'best ROI', 'most profitable', 'good margins', 'high profit', 'good profit margin', 'excellent margins', 'strong profitability', 'high returns'; "
    "negative weight: 'low margin', 'poor profit', 'low profitability', 'weak margins', 'minimal profit', 'low returns', 'poor ROI', 'unprofitable'; "
    "0 should be used if no preference for the profit margin."
)

return_rate_description = (
    "Weight for return rate optimization. "
    "Higher weight means preference for products with HIGHER return rates. "
    "example: 'high return rate', 'faulty products', 'returns'"
)

sales_performance_description = (
    "Weight for sales performance. "
    "Higher weight means preference for HIGH-SELLING products. "
    "Weight depends on the adjective or noun used to describe the sales performance. "
    "For example: "
    "positive weight: 'popular', 'best-selling', 'high demand', 'top performers', 'trending', 'bestsellers', 'high sales', 'strong sales', 'excellent sales', 'top selling', 'most sold'; "
    "negative weight: 'low sales', 'poor performance', 'slow selling', 'low demand', 'unpopular', 'least sold', 'weak sales', 'poor sales', 'minimal sales'; "
    "0 should be used if no preference for the sales performance."
)

revenue_performance_description = (
    "Weight for revenue performance. "
    "Higher weight means preference for HIGH-REVENUE generating products. "
    "Weight depends on the adjective or noun used to describe the revenue performance. "
    "For example: "
    "positive weight: 'high revenue', 'top earning', 'revenue generators', 'high revenue products', 'strong revenue', 'excellent revenue', 'best revenue', 'most revenue', 'highest revenue'; "
    "negative weight: 'low revenue', 'poor revenue', 'minimal revenue', 'weak revenue', 'least revenue', 'low earning', 'poor earning', 'minimal earning'; "
    "0 should be used if no preference for the revenue performance."
)

product_description = (
    "Product characteristics to search for. Should include the product specifications, "
    "specific features, or use cases. "
    "Examples: 'women shoes', 'electronics', 'athletic wear', 'denim jeans', "
    "'winter clothing', 'accessories', 'designer brands', 'casual wear'. "
    "If no specific product description mentioned, leave empty."
)

brand_description = (
    "Brand filter. Include brands that should be included in search. "
    "Available brands: Holden, Nike, Adidas, etc. "
    "Use when user specifically mentions a brand."
)

department_description = (
    "Department filter. Include departments that should be included in search. "
    "Available departments: Women, Men, Kids. "
    "Use when user specifically mentions gender or age group."
)

category_description = (
    "Product category filter. Include specific categories mentioned by user. "
    "Available categories: Accessories, Plus, Swim, Active, Socks & Hosiery, Socks, Dresses, "
    "Pants & Capris, Fashion Hoodies & Sweatshirts, Skirts, Blazers & Jackets, Suits, "
    "Tops & Tees, Sweaters, Shorts, Jeans, Maternity, Sleep & Lounge, Suits & Sport Coats, "
    "Pants, Intimates, Outerwear & Coats, Underwear, Leggings, Jumpsuits & Rompers, Clothing Sets."
)

system_prompt = (
    "You are a procurement assistant that extracts search parameters from business queries. "
    "Focus on business objectives like cost optimization, supplier reliability, "
    "product performance, and specific product requirements. "
    "Consider seasonal trends, inventory turnover, and strategic sourcing needs. "
    "\n\nKey guidelines:\n"
    "- Extract product characteristics for 'product_description'\n"
    "- Set weights based on business priorities mentioned\n"
    "- Use filters for specific departments or categories\n"
    "- Consider procurement context (bulk buying, supplier evaluation, etc.)\n"
    "- Weight values should be 0 (not important) to 10 (very important)"
)