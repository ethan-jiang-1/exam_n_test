"""
Intermediate Pydantic Validator Examples
=====================================

This module demonstrates various validation techniques in Pydantic, including:
1. Custom validators
2. Field validators
3. Model validators
4. Validation dependencies
5. Pre/post validation processing

Key concepts covered:
- Custom validation logic
- Validator decorators
- Validation chaining
- Error handling in validators
"""

from typing import Any, List, Optional
from typing_extensions import Annotated
from pydantic import (
    BaseModel,
    ValidationError,
    field_validator,
    model_validator,
    AfterValidator
)
import rich


def check_squares(v: int) -> int:
    """Validates if a number is a perfect square."""
    assert v**0.5 % 1 == 0, f'{v} is not a square number'
    return v


def double(v: Any) -> Any:
    """Doubles the input value."""
    return v * 2


# Custom type with chained validators
SquareNumber = Annotated[int, AfterValidator(double), AfterValidator(check_squares)]


class ValidatedModel(BaseModel):
    """
    A model demonstrating field and model validators.
    
    Attributes:
        numbers: List of numbers that must be perfect squares after doubling
        name: String that will be capitalized
        code: Optional string that must be in specific format
    """
    numbers: List[SquareNumber]
    name: str
    code: Optional[str] = None

    @field_validator('name')
    def capitalize_name(cls, v: str) -> str:
        """Capitalizes the name field."""
        return v.capitalize()

    @field_validator('code')
    def validate_code(cls, v: Optional[str]) -> Optional[str]:
        """Validates the code format if present."""
        if v is None:
            return v
        if not v.startswith('CODE_'):
            raise ValueError('Code must start with CODE_')
        return v

    @model_validator(mode='after')
    def check_name_code_match(self) -> 'ValidatedModel':
        """Ensures code matches name if present."""
        if self.code is not None and self.name.lower() not in self.code.lower():
            raise ValueError('Code must contain the name')
        return self


def demonstrate_field_validation():
    """Demonstrates field-level validation."""
    valid_data = {
        'numbers': [2, 8],  # Will become [4, 16] after doubling
        'name': 'john',
        'code': 'CODE_JOHN_123'
    }

    try:
        model = ValidatedModel(**valid_data)
        rich.print("\n=== Valid Model ===")
        rich.print(model)
        rich.print("Numbers after validation:", model.numbers)
        rich.print("Name after capitalization:", model.name)
    except ValidationError as e:
        rich.print("Validation Error:", e)


def demonstrate_validation_errors():
    """Demonstrates various validation error scenarios."""
    test_cases = [
        {
            'case': "Invalid square numbers",
            'data': {
                'numbers': [2, 4],  # 4 and 8 after doubling - 8 is not a square
                'name': 'alice',
                'code': 'CODE_ALICE_123'
            }
        },
        {
            'case': "Invalid code format",
            'data': {
                'numbers': [2, 8],
                'name': 'bob',
                'code': 'INVALID_CODE'  # Doesn't start with CODE_
            }
        },
        {
            'case': "Code doesn't match name",
            'data': {
                'numbers': [2, 8],
                'name': 'charlie',
                'code': 'CODE_DAVID_123'  # Contains different name
            }
        }
    ]

    for test_case in test_cases:
        rich.print(f"\n=== Testing: {test_case['case']} ===")
        try:
            model = ValidatedModel(**test_case['data'])
            rich.print(model)
        except ValidationError as e:
            rich.print("Validation Error:")
            rich.print(e.json(indent=2))


class AdvancedValidation(BaseModel):
    """
    Demonstrates more advanced validation techniques.
    
    Attributes:
        items: List of strings that will be processed
        total: Number that must match items count
    """
    items: List[str]
    total: int

    @field_validator('items')
    def clean_items(cls, v: List[str]) -> List[str]:
        """Cleans and validates items."""
        return [item.strip().lower() for item in v if item.strip()]

    @model_validator(mode='after')
    def validate_total(self) -> 'AdvancedValidation':
        """Ensures total matches the number of items."""
        if len(self.items) != self.total:
            raise ValueError(f'Total must match number of items. Expected {len(self.items)}, got {self.total}')
        return self


def demonstrate_advanced_validation():
    """Demonstrates advanced validation features."""
    test_data = {
        'items': ['  Item1  ', 'ITEM2', ' item3 '],
        'total': 3
    }

    try:
        model = AdvancedValidation(**test_data)
        rich.print("\n=== Advanced Validation ===")
        rich.print("Original items:", test_data['items'])
        rich.print("Cleaned items:", model.items)
    except ValidationError as e:
        rich.print("Validation Error:", e)


if __name__ == "__main__":
    demonstrate_field_validation()
    demonstrate_validation_errors()
    demonstrate_advanced_validation() 