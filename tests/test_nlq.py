"""
Unit tests for the natural language query processing module.
"""
import pytest
from superlinked_app.nlq import (
    cost_description,
    reliability_description, 
    profit_margin_description,
    return_rate_description,
    sales_performance_description,
    revenue_performance_description,
    product_description,
    brand_description,
    department_description,
    category_description,
    system_prompt
)


class TestDescriptions:
    """Test the parameter descriptions for natural language processing."""

    def test_cost_description_content(self):
        """Test that cost description contains key guidance."""
        assert "Weight for cost optimization" in cost_description
        assert "LOWER cost products" in cost_description
        assert "cheap" in cost_description
        assert "affordable" in cost_description
        assert "expensive" in cost_description
        assert "premium" in cost_description

    def test_reliability_description_content(self):
        """Test that reliability description contains key guidance."""
        assert "Weight for supplier reliability" in reliability_description
        assert "MORE reliable suppliers" in reliability_description
        assert "reliable" in reliability_description
        assert "trustworthy" in reliability_description
        assert "consistent" in reliability_description

    def test_profit_margin_description_content(self):
        """Test that profit margin description contains key guidance."""
        assert "Weight for profit margin optimization" in profit_margin_description
        assert "BETTER margins" in profit_margin_description
        assert "profitable" in profit_margin_description
        assert "high margin" in profit_margin_description
        assert "low margin" in profit_margin_description

    def test_return_rate_description_content(self):
        """Test that return rate description contains key guidance."""
        assert "Weight for return rate optimization" in return_rate_description
        assert "HIGHER return rates" in return_rate_description
        assert "return rate" in return_rate_description

    def test_sales_performance_description_content(self):
        """Test that sales performance description contains key guidance."""
        assert "Weight for sales performance" in sales_performance_description
        assert "HIGH-SELLING products" in sales_performance_description
        assert "popular" in sales_performance_description
        assert "best-selling" in sales_performance_description
        assert "low sales" in sales_performance_description

    def test_revenue_performance_description_content(self):
        """Test that revenue performance description contains key guidance."""
        assert "Weight for revenue performance" in revenue_performance_description
        assert "HIGH-REVENUE generating products" in revenue_performance_description
        assert "high revenue" in revenue_performance_description
        assert "revenue generators" in revenue_performance_description

    def test_product_description_content(self):
        """Test that product description contains examples."""
        assert "Product characteristics to search for" in product_description
        assert "women shoes" in product_description
        assert "electronics" in product_description
        assert "denim jeans" in product_description

    def test_department_description_content(self):
        """Test that department description contains available options."""
        assert "Department filter" in department_description
        assert "Women" in department_description
        assert "Men" in department_description
        assert "Kids" in department_description

    def test_category_description_content(self):
        """Test that category description contains available options."""
        assert "Product category filter" in category_description
        assert "Jeans" in category_description
        assert "Dresses" in category_description
        assert "Accessories" in category_description

    def test_brand_description_content(self):
        """Test that brand description mentions filtering."""
        assert "Brand filter" in brand_description
        assert "brands" in brand_description.lower()


class TestSystemPrompt:
    """Test the system prompt for LLM interaction."""

    def test_system_prompt_structure(self):
        """Test that system prompt contains essential elements."""
        assert "procurement assistant" in system_prompt
        assert "business objectives" in system_prompt
        assert "cost optimization" in system_prompt
        assert "supplier reliability" in system_prompt

    def test_system_prompt_guidelines(self):
        """Test that system prompt includes key guidelines."""
        assert "Key guidelines:" in system_prompt
        assert "product_description" in system_prompt
        assert "business priorities" in system_prompt
        assert "Weight values should be 0" in system_prompt
        assert "10 (very important)" in system_prompt

    def test_system_prompt_context_awareness(self):
        """Test that system prompt emphasizes procurement context."""
        assert "procurement context" in system_prompt
        assert "bulk buying" in system_prompt
        assert "supplier evaluation" in system_prompt
        assert "seasonal trends" in system_prompt
        assert "inventory turnover" in system_prompt


class TestDescriptionConsistency:
    """Test consistency across all description strings."""

    def test_all_descriptions_are_strings(self):
        """Test that all descriptions are string types."""
        descriptions = [
            cost_description,
            reliability_description,
            profit_margin_description,
            return_rate_description,
            sales_performance_description,
            revenue_performance_description,
            product_description,
            brand_description,
            department_description,
            category_description,
            system_prompt
        ]
        
        for desc in descriptions:
            assert isinstance(desc, str), f"Description is not a string: {type(desc)}"

    def test_descriptions_not_empty(self):
        """Test that no descriptions are empty."""
        descriptions = [
            cost_description,
            reliability_description,
            profit_margin_description,
            return_rate_description,
            sales_performance_description,
            revenue_performance_description,
            product_description,
            brand_description,
            department_description,
            category_description,
            system_prompt
        ]
        
        for desc in descriptions:
            assert len(desc.strip()) > 0, "Description is empty"

    def test_weight_descriptions_mention_weight(self):
        """Test that weight-related descriptions mention 'weight'."""
        weight_descriptions = [
            cost_description,
            reliability_description,
            profit_margin_description,
            return_rate_description,
            sales_performance_description,
            revenue_performance_description
        ]
        
        for desc in weight_descriptions:
            assert "weight" in desc.lower(), f"Weight description missing 'weight': {desc[:50]}..."

    def test_filter_descriptions_mention_filter(self):
        """Test that filter descriptions mention filtering concepts."""
        filter_descriptions = [
            brand_description,
            department_description,
            category_description
        ]
        
        for desc in filter_descriptions:
            assert any(word in desc.lower() for word in ['filter', 'include', 'available']), \
                f"Filter description missing filter concepts: {desc[:50]}..."


@pytest.mark.unit
class TestDescriptionUsability:
    """Test that descriptions are usable for LLM prompt engineering."""

    def test_positive_negative_examples(self):
        """Test that weight descriptions include positive and negative examples."""
        descriptions_with_examples = [
            cost_description,
            reliability_description,
            profit_margin_description,
            sales_performance_description,
            revenue_performance_description
        ]
        
        for desc in descriptions_with_examples:
            # Should contain examples of positive and negative keywords
            assert any(word in desc for word in ['Positive:', 'positive weight:', 'example:']), \
                f"Description missing positive examples: {desc[:50]}..."

    def test_practical_keywords_included(self):
        """Test that descriptions include practical business keywords."""
        # Cost-related keywords
        assert "cheap" in cost_description
        assert "budget" in cost_description
        assert "expensive" in cost_description
        
        # Reliability keywords
        assert "reliable" in reliability_description
        assert "dependable" in reliability_description
        
        # Performance keywords
        assert "popular" in sales_performance_description
        assert "best-selling" in sales_performance_description

    def test_business_context_keywords(self):
        """Test that system prompt includes business context keywords."""
        business_keywords = [
            "procurement",
            "business",
            "supplier",
            "inventory",
            "strategic sourcing"
        ]
        
        for keyword in business_keywords:
            assert keyword in system_prompt.lower(), f"Missing business keyword: {keyword}"

    def test_description_length_reasonable(self):
        """Test that descriptions are neither too short nor too long."""
        descriptions = [
            cost_description,
            reliability_description,
            profit_margin_description,
            system_prompt
        ]
        
        for desc in descriptions:
            # Should be substantial but not overwhelming
            assert 50 <= len(desc) <= 2000, \
                f"Description length unreasonable: {len(desc)} chars"


class TestPromptEngineering:
    """Test aspects important for effective prompt engineering."""

    def test_clear_instruction_format(self):
        """Test that descriptions provide clear instructions to the LLM."""
        weight_descriptions = [
            cost_description,
            profit_margin_description,
            sales_performance_description
        ]
        
        for desc in weight_descriptions:
            # Should explain what higher weight means
            assert "higher weight" in desc.lower(), \
                f"Description unclear about weight meaning: {desc[:50]}..."

    def test_example_driven_guidance(self):
        """Test that descriptions provide concrete examples."""
        assert "women shoes" in product_description
        assert "electronics" in product_description
        assert "denim jeans" in product_description
        
        # Categories should list actual options
        assert "Accessories" in category_description
        assert "Jeans" in category_description

    def test_neutral_weight_guidance(self):
        """Test that descriptions explain when to use neutral weights."""
        neutral_guidance_descriptions = [
            cost_description,
            profit_margin_description,
            sales_performance_description,
            revenue_performance_description
        ]
        
        for desc in neutral_guidance_descriptions:
            assert "0" in desc or "neutral" in desc.lower(), \
                f"Description missing neutral weight guidance: {desc[:50]}..." 