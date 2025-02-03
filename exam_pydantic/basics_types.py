"""
Basic Pydantic Type System Examples
=================================

This module demonstrates the various types supported by Pydantic, including:
1. Basic Python types
2. Collection types
3. Literal types
4. Enum types
5. Optional and Union types

Key concepts covered:
- Type annotations
- Type validation
- Complex type structures
- Literal type constraints
"""

from typing import Dict, List, Literal, Optional, Tuple, Union
from enum import Enum
from pydantic import BaseModel
import rich


class Color(str, Enum):
    """Enum for color choices"""
    RED = 'red'
    GREEN = 'green'
    BLUE = 'blue'


class Fruit(BaseModel):
    """
    A model demonstrating various type annotations.
    
    Attributes:
        name: The name of the fruit
        color: Must be one of the predefined colors
        weight: Weight in grams
        tags: List of string tags
        metadata: Dictionary with mixed value types
    """
    name: str
    color: Literal['red', 'green', 'blue']  # Using Literal for fixed choices
    weight: float
    tags: List[str] = []  # List type with default
    metadata: Dict[str, Union[int, float, str]]  # Dict with mixed value types


class ComplexTypes(BaseModel):
    """
    A model demonstrating more complex type combinations.
    
    Attributes:
        mixed_list: List that can contain both integers and strings
        coordinates: Tuple of exactly two floats
        nested_dict: Dictionary with nested structure
        optional_value: Optional string field
    """
    mixed_list: List[Union[int, str]]
    coordinates: Tuple[float, float]
    nested_dict: Dict[str, Dict[str, int]]
    optional_value: Optional[str] = None


def demonstrate_basic_types():
    """Demonstrates basic type validation and usage."""
    # Valid fruit example
    fruit_data = {
        'name': 'Apple',
        'color': 'red',
        'weight': 150.5,
        'tags': ['sweet', 'fresh'],
        'metadata': {
            'origin': 'USA',
            'price': 1.99,
            'stock': 100
        }
    }

    fruit = Fruit(**fruit_data)
    rich.print("\n=== Basic Types Example ===")
    rich.print(fruit)
    
    # Demonstrate type checking
    rich.print("\nType checks:")
    rich.print(f"name is str: {isinstance(fruit.name, str)}")
    rich.print(f"weight is float: {isinstance(fruit.weight, float)}")
    rich.print(f"tags is list: {isinstance(fruit.tags, list)}")


def demonstrate_complex_types():
    """Demonstrates more complex type combinations."""
    complex_data = {
        'mixed_list': [1, "two", 3, "four"],
        'coordinates': (10.5, 20.7),
        'nested_dict': {
            'section1': {'value': 1},
            'section2': {'value': 2}
        },
        'optional_value': 'present'
    }

    complex_obj = ComplexTypes(**complex_data)
    rich.print("\n=== Complex Types Example ===")
    rich.print(complex_obj)
    
    # Try without optional value
    del complex_data['optional_value']
    complex_obj = ComplexTypes(**complex_data)
    rich.print("\n=== With Optional Value Omitted ===")
    rich.print(complex_obj)


def demonstrate_enum_types():
    """Demonstrates using Enum types."""
    class Product(BaseModel):
        name: str
        color: Color

    # Create products with different colors
    products = [
        Product(name="Item 1", color=Color.RED),
        Product(name="Item 2", color=Color.GREEN),
        Product(name="Item 3", color=Color.BLUE)
    ]

    rich.print("\n=== Enum Types Example ===")
    for product in products:
        rich.print(f"{product.name}: {product.color}")
        rich.print(f"Color value: {product.color.value}")


if __name__ == "__main__":
    demonstrate_basic_types()
    demonstrate_complex_types()
    demonstrate_enum_types() 