"""
Unit tests for the schema module.
"""
import pytest
from superlinked_app.schema import ProductSchema, product_schema
from superlinked import framework as sl


class TestProductSchema:
    """Test the ProductSchema class definition."""

    def test_product_schema_instance(self):
        """Test that product_schema is properly instantiated."""
        assert isinstance(product_schema, ProductSchema)
        assert isinstance(product_schema, sl.Schema)

    def test_product_schema_fields(self):
        """Test that all expected fields are present in the schema."""
        # Check ID field
        assert hasattr(product_schema, 'product_id')
        assert isinstance(product_schema.product_id, sl.IdField)
        
        # Check text fields
        text_fields = ['name', 'category', 'brand', 'department']
        for field_name in text_fields:
            assert hasattr(product_schema, field_name)
            field = getattr(product_schema, field_name)
            assert isinstance(field, sl.String)
        
        # Check float fields
        float_fields = [
            'cost', 'retail_price', 'profit_margin_percent',
            'return_rate_percent', 'supplier_reliability_score',
            'avg_sale_price', 'total_revenue', 'daily_sales_rate'
        ]
        for field_name in float_fields:
            assert hasattr(product_schema, field_name)
            field = getattr(product_schema, field_name)
            assert isinstance(field, sl.Float)
            
        # Check integer fields
        integer_fields = ['total_orders', 'days_since_creation', 'total_items_sold']
        for field_name in integer_fields:
            assert hasattr(product_schema, field_name)
            field = getattr(product_schema, field_name)
            assert isinstance(field, sl.Integer)

    def test_schema_field_types_correctness(self):
        """Test that field types match expected Superlinked types."""
        schema = product_schema
        
        # Test specific field type mappings
        assert isinstance(schema.product_id, sl.IdField)
        assert isinstance(schema.name, sl.String)
        assert isinstance(schema.cost, sl.Float)
        assert isinstance(schema.total_orders, sl.Integer)

    def test_schema_completeness(self):
        """Test that the schema includes all business-critical fields."""
        required_business_fields = [
            'product_id',        # Identity
            'name',              # Product identification
            'category',          # Classification
            'brand',             # Supplier/brand info
            'department',        # Business segment
            'cost',              # Procurement cost
            'retail_price',      # Selling price
            'profit_margin_percent',  # Profitability
            'total_orders',      # Sales volume
            'return_rate_percent',    # Quality metric
            'supplier_reliability_score',  # Supplier assessment
            'total_revenue',     # Revenue performance
        ]
        
        for field in required_business_fields:
            assert hasattr(product_schema, field), f"Missing critical field: {field}"

    def test_schema_field_count(self):
        """Test that we have the expected number of fields."""
        # Count all schema attributes that are Superlinked field types
        field_count = 0
        for attr_name in dir(product_schema):
            if not attr_name.startswith('_'):  # Skip private attributes
                attr = getattr(product_schema, attr_name)
                if isinstance(attr, (sl.IdField, sl.String, sl.Float, sl.Integer)):
                    field_count += 1
        
        # We expect 17 fields based on the schema definition
        expected_fields = 17
        assert field_count == expected_fields, f"Expected {expected_fields} fields, got {field_count}"

    def test_schema_instantiation_multiple_times(self):
        """Test that creating multiple schema instances works correctly."""
        schema1 = ProductSchema()
        schema2 = ProductSchema()
        
        # They should be different instances
        assert schema1 is not schema2
        
        # But should have the same field structure
        assert type(schema1.product_id) == type(schema2.product_id)
        assert type(schema1.name) == type(schema2.name)
        assert type(schema1.cost) == type(schema2.cost)


class TestSchemaFieldProperties:
    """Test specific properties and behaviors of schema fields."""

    def test_id_field_properties(self):
        """Test properties of the ID field."""
        id_field = product_schema.product_id
        assert isinstance(id_field, sl.IdField)
        # ID fields should be unique identifiers
        assert hasattr(id_field, '__class__')

    def test_string_field_properties(self):
        """Test properties of string fields."""
        string_fields = [product_schema.name, product_schema.category, 
                        product_schema.brand, product_schema.department]
        
        for field in string_fields:
            assert isinstance(field, sl.String)

    def test_numeric_field_properties(self):
        """Test properties of numeric fields."""
        # Float fields should be monetary or percentage values
        float_fields = [
            product_schema.cost,
            product_schema.retail_price, 
            product_schema.profit_margin_percent,
            product_schema.return_rate_percent,
            product_schema.supplier_reliability_score,
            product_schema.avg_sale_price,
            product_schema.total_revenue,
            product_schema.daily_sales_rate
        ]
        
        for field in float_fields:
            assert isinstance(field, sl.Float)
            
        # Integer fields should be count-based metrics
        integer_fields = [
            product_schema.total_orders,
            product_schema.days_since_creation,
            product_schema.total_items_sold
        ]
        
        for field in integer_fields:
            assert isinstance(field, sl.Integer)


@pytest.mark.unit
class TestSchemaUsagePatterns:
    """Test how the schema would be used in typical scenarios."""

    def test_schema_field_access(self):
        """Test that schema fields can be accessed properly."""
        schema = product_schema
        
        # Should be able to access all fields without errors
        try:
            _ = schema.product_id
            _ = schema.name
            _ = schema.category
            _ = schema.cost
            _ = schema.profit_margin_percent
            _ = schema.total_orders
        except AttributeError as e:
            pytest.fail(f"Schema field access failed: {e}")

    def test_schema_field_comparison_operations(self):
        """Test that schema fields support comparison operations for queries."""
        schema = product_schema
        
        # These operations should not raise errors (they return filter objects)
        try:
            _ = schema.cost >= 10.0
            _ = schema.cost <= 100.0
            _ = schema.profit_margin_percent >= 50.0
            _ = schema.total_orders >= 1
            _ = schema.return_rate_percent <= 5.0
        except Exception as e:
            pytest.fail(f"Schema field comparison failed: {e}")

    def test_schema_field_in_operations(self):
        """Test that schema fields support 'in' operations for categorical filtering."""
        schema = product_schema
        
        # These operations should work for categorical fields
        try:
            _ = schema.department.in_(["Women", "Men", "Kids"])
            _ = schema.category.in_(["Jeans", "Dresses", "Accessories"])
            _ = schema.brand.in_(["Nike", "Adidas", "TestBrand"])
        except Exception as e:
            pytest.fail(f"Schema field 'in' operation failed: {e}") 