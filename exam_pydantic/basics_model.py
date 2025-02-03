"""
Basic Pydantic Model Examples
============================

This module demonstrates the fundamental usage of Pydantic models, including:
1. Basic model definition
2. Type annotations
3. Model instantiation
4. Basic validation
5. Model methods

Key concepts covered:
- BaseModel inheritance
- Type hints
- Nested models
- Basic error handling
"""

from typing import List
from pydantic import BaseModel, ValidationError
import rich


class Address(BaseModel):
    """
    A simple model representing an address.
    
    Attributes:
        street (str): The street name
        building (int): The building number
    """
    street: str
    building: int


class Person(BaseModel):
    """
    A model demonstrating nested models and various field types.
    
    Attributes:
        age (int): Person's age
        name (str): Person's name
        is_married (bool): Marriage status
        address (Address): Nested address model
        languages (List[str]): List of language codes
    """
    age: int
    name: str
    is_married: bool
    address: Address
    languages: List[str]


def demonstrate_valid_model():
    """Demonstrates creating and using a valid model instance."""
    # Valid data example
    valid_data = {
        'age': 30,
        'name': 'John Doe',
        'is_married': False,
        'address': {
            'street': 'Main Street',
            'building': 123
        },
        'languages': ['en-us', 'es-es']
    }

    try:
        # Create model instance
        person = Person(**valid_data)
        
        # Demonstrate different ways to access data
        rich.print("=== Model Instance ===")
        rich.print(person)
        
        rich.print("\n=== Accessing Individual Fields ===")
        print(f"Name: {person.name}")
        print(f"Age: {person.age}")
        print(f"Address: {person.address.street}, {person.address.building}")
        
        rich.print("\n=== Model Methods ===")
        rich.print("model_dump():", person.model_dump())
        rich.print("model_dump_json():", person.model_dump_json())
        
        return person
    
    except ValidationError as e:
        rich.print("Validation Error:", e)
        return None


def demonstrate_invalid_model():
    """Demonstrates validation errors with invalid data."""
    # Invalid data example
    invalid_data = {
        'age': "not an integer",  # Wrong type
        'name': 123,              # Wrong type
        'is_married': "false",    # Wrong type
        'address': {
            'street': None,       # Wrong type
            'building': "123"     # Wrong type
        },
        'languages': [123, 456]   # Wrong type in list
    }

    try:
        person = Person(**invalid_data)
        return person
    
    except ValidationError as e:
        rich.print("\n=== Validation Error Example ===")
        rich.print("Error as string:", str(e))
        rich.print("\nError as JSON:", e.json())
        return None


if __name__ == "__main__":
    print("\n=== Valid Model Example ===")
    demonstrate_valid_model()
    
    print("\n=== Invalid Model Example ===")
    demonstrate_invalid_model() 