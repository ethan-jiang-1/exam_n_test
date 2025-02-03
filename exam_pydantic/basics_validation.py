"""
Basic Pydantic Validation Examples
================================

This module demonstrates the fundamental validation features in Pydantic, including:
1. Field constraints
2. Required vs Optional fields
3. Validation error handling
4. Error message formatting

Key concepts covered:
- Field validation
- Error handling
- Constraint checking
- Error message formatting
"""

from typing import Optional
from pydantic import BaseModel, Field, ValidationError
import rich


class UserProfile(BaseModel):
    """
    A model demonstrating various field validations.
    
    Attributes:
        username: Required, 3-20 characters
        age: Optional, must be between 0 and 150
        email: Required, must contain @ symbol
        score: Required, must be between 0 and 100
    """
    username: str = Field(..., min_length=3, max_length=20)
    age: Optional[int] = Field(None, ge=0, le=150)
    email: str = Field(..., pattern=r".*@.*")
    score: float = Field(..., ge=0, le=100)


def demonstrate_field_validation():
    """Demonstrates field-level validation with constraints."""
    # Valid data example
    valid_data = {
        'username': 'john_doe',
        'age': 25,
        'email': 'john@example.com',
        'score': 85.5
    }

    try:
        user = UserProfile(**valid_data)
        rich.print("\n=== Valid User Profile ===")
        rich.print(user)
        return user
    
    except ValidationError as e:
        rich.print("Validation Error:", e)
        return None


def demonstrate_validation_errors():
    """Demonstrates various validation error scenarios."""
    # Test cases with different validation errors
    test_cases = [
        {
            'case': "Username too short",
            'data': {
                'username': 'jo',  # Too short
                'email': 'john@example.com',
                'score': 85.5
            }
        },
        {
            'case': "Invalid age",
            'data': {
                'username': 'john_doe',
                'age': 200,  # Too high
                'email': 'john@example.com',
                'score': 85.5
            }
        },
        {
            'case': "Invalid email",
            'data': {
                'username': 'john_doe',
                'email': 'invalid-email',  # Missing @
                'score': 85.5
            }
        },
        {
            'case': "Score out of range",
            'data': {
                'username': 'john_doe',
                'email': 'john@example.com',
                'score': 150  # Over 100
            }
        }
    ]

    for test_case in test_cases:
        rich.print(f"\n=== Testing: {test_case['case']} ===")
        try:
            user = UserProfile(**test_case['data'])
            rich.print(user)
        except ValidationError as e:
            rich.print("Validation Error:")
            rich.print(e.json(indent=2))


def demonstrate_error_handling():
    """Demonstrates different ways to handle and format validation errors."""
    invalid_data = {
        'username': 'x',
        'age': -5,
        'email': 'not-an-email',
        'score': 999
    }

    try:
        UserProfile(**invalid_data)
    except ValidationError as e:
        rich.print("\n=== Different Error Formats ===")
        
        rich.print("\nAs String:")
        rich.print(str(e))
        
        rich.print("\nAs JSON:")
        rich.print(e.json(indent=2))
        
        rich.print("\nAs Error Objects:")
        for error in e.errors():
            rich.print(f"Field: {error['loc']}")
            rich.print(f"Error: {error['msg']}")
            rich.print(f"Type: {error['type']}\n")


if __name__ == "__main__":
    demonstrate_field_validation()
    demonstrate_validation_errors()
    demonstrate_error_handling() 