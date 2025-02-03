"""
Advanced Pydantic Validator Examples
=================================

This module demonstrates advanced validation techniques in Pydantic, including:
1. Wrap validators
2. Mode-specific validation
3. Complex validation chains
4. Context-aware validation
5. Custom error handling

Key concepts covered:
- WrapValidator usage
- Validation modes (python vs json)
- Validation context
- Advanced error handling
"""

from typing import Any, List, Optional
from typing_extensions import Annotated
from pydantic import (
    BaseModel,
    ValidationError,
    ValidationInfo,
    ValidatorFunctionWrapHandler,
    WrapValidator
)
import rich
import json


def maybe_strip_whitespace(
    v: Any, 
    handler: ValidatorFunctionWrapHandler, 
    info: ValidationInfo
) -> int:
    """
    Mode-aware validator that handles both JSON and Python inputs differently.
    
    Args:
        v: The value to validate
        handler: The validation handler
        info: Validation context information
    
    Returns:
        Processed integer value
    """
    if info.mode == 'json':
        assert isinstance(v, str), 'In JSON mode the input must be a string!'
        try:
            return handler(v)
        except ValidationError:
            return handler(v.strip())
    
    assert info.mode == 'python'
    assert isinstance(v, int), 'In Python mode the input must be an int!'
    return v


# Define custom type with wrap validator
ProcessedNumber = Annotated[int, WrapValidator(maybe_strip_whitespace)]


class ContextAwareModel(BaseModel):
    """
    A model demonstrating context-aware validation.
    
    Attributes:
        numbers: List of numbers that are processed differently based on input mode
        mode: String indicating the current processing mode
    """
    numbers: List[ProcessedNumber]
    mode: str = 'default'


def demonstrate_json_mode():
    """Demonstrates validation in JSON mode."""
    # JSON string with whitespace-padded numbers
    json_data = json.dumps({
        'numbers': [' 123 ', '  456  ', ' 789 '],
        'mode': 'json'
    })

    try:
        model = ContextAwareModel.model_validate_json(json_data)
        rich.print("\n=== JSON Mode Validation ===")
        rich.print("Original JSON:", json_data)
        rich.print("Processed Model:", model)
    except ValidationError as e:
        rich.print("Validation Error:", e)


def demonstrate_python_mode():
    """Demonstrates validation in Python mode."""
    # Direct Python dictionary with integers
    python_data = {
        'numbers': [123, 456, 789],
        'mode': 'python'
    }

    try:
        model = ContextAwareModel(**python_data)
        rich.print("\n=== Python Mode Validation ===")
        rich.print("Original Data:", python_data)
        rich.print("Processed Model:", model)
    except ValidationError as e:
        rich.print("Validation Error:", e)


def demonstrate_validation_errors():
    """Demonstrates various validation error scenarios."""
    test_cases = [
        {
            'case': "Invalid JSON input type",
            'data': {
                'numbers': [True, False],  # Wrong type in JSON mode
                'mode': 'json'
            }
        },
        {
            'case': "Invalid Python input type",
            'data': {
                'numbers': ['123', '456'],  # Strings in Python mode
                'mode': 'python'
            }
        }
    ]

    for test_case in test_cases:
        rich.print(f"\n=== Testing: {test_case['case']} ===")
        try:
            model = ContextAwareModel(**test_case['data'])
            rich.print(model)
        except ValidationError as e:
            rich.print("Validation Error:")
            rich.print(e.json(indent=2))


class ComplexValidation(BaseModel):
    """
    Demonstrates complex validation scenarios.
    
    Attributes:
        raw_data: String that needs to be parsed and validated
        processed_data: Optional processed version of raw_data
    """
    raw_data: str
    processed_data: Optional[List[int]] = None

    def process_raw_data(self) -> List[int]:
        """Processes raw string data into integers."""
        try:
            # Split by commas and convert to integers
            values = [int(x.strip()) for x in self.raw_data.split(',')]
            return values
        except ValueError as e:
            raise ValueError(f"Failed to process raw data: {e}")

    def model_post_init(self, __context: Any) -> None:
        """Post-initialization processing."""
        if self.raw_data and self.processed_data is None:
            self.processed_data = self.process_raw_data()


def demonstrate_complex_validation():
    """Demonstrates complex validation scenarios."""
    test_cases = [
        {
            'case': "Valid raw data",
            'data': {'raw_data': "1, 2, 3, 4, 5"}
        },
        {
            'case': "Invalid raw data",
            'data': {'raw_data': "1, 2, invalid, 4, 5"}
        }
    ]

    for test_case in test_cases:
        rich.print(f"\n=== Testing: {test_case['case']} ===")
        try:
            model = ComplexValidation(**test_case['data'])
            rich.print("Raw data:", model.raw_data)
            rich.print("Processed data:", model.processed_data)
        except ValidationError as e:
            rich.print("Validation Error:")
            rich.print(e.json(indent=2))


if __name__ == "__main__":
    demonstrate_json_mode()
    demonstrate_python_mode()
    demonstrate_validation_errors()
    demonstrate_complex_validation() 