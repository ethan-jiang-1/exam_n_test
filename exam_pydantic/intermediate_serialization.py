"""
Intermediate Pydantic Serialization Examples
========================================

This module demonstrates advanced serialization features in Pydantic, including:
1. Custom serialization
2. Multiple formats
3. Serialization hooks
4. Complex type handling
5. Alias and exclude options

Key concepts covered:
- JSON serialization
- Custom encoders
- Export formats
- Serialization control
"""

from datetime import datetime, date
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field, ConfigDict
import rich


class UserStatus(str, Enum):
    """User status enumeration."""
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    PENDING = 'pending'


class CustomSerializationModel(BaseModel):
    """
    Model demonstrating custom serialization.
    
    Attributes:
        created_at: Timestamp that will be serialized as ISO format
        updated_at: Optional timestamp
        data: Dictionary with custom serialization
    """
    model_config = ConfigDict(
        json_encoders={
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }
    )
    
    created_at: datetime
    updated_at: Optional[datetime] = None
    data: Dict[str, Any] = {}


class UserProfile(BaseModel):
    """
    User profile with various serialization options.
    
    Attributes:
        user_id: UUID field
        username: User's name
        status: User's status
        tags: List of tags
        last_login: Last login date
        settings: User settings
    """
    user_id: UUID = Field(default_factory=uuid4)
    username: str = Field(alias='user_name')
    status: UserStatus = UserStatus.PENDING
    tags: List[str] = []
    last_login: Optional[date] = None
    settings: Dict[str, Any] = {}

    def model_dump(
        self,
        *,
        include: Optional[set[str]] = None,
        exclude: Optional[set[str]] = None,
        by_alias: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """Customized model dump with additional options."""
        data = super().model_dump(
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            **kwargs
        )
        
        # Add computed field
        data['is_active'] = (self.status == UserStatus.ACTIVE)
        return data


def demonstrate_basic_serialization():
    """Demonstrate basic serialization features."""
    model = CustomSerializationModel(
        created_at=datetime(2025, 2, 3, 21, 41, 33, 15321),
        updated_at=datetime(2025, 2, 3, 21, 41, 33, 15330),
        data={'key': 'value', 'number': 42}
    )
    
    print("=== Basic Serialization ===")
    print("Model:")
    print(model)
    print("JSON: ")
    print(model.model_dump_json())
    print("Dict:")
    print(model.model_dump())


def demonstrate_serialization_options():
    """Demonstrate various serialization options."""
    user = UserProfile(
        user_name='john_doe',  # Using the alias
        status=UserStatus.ACTIVE,
        tags=['premium', 'verified'],
        last_login=date(2025, 1, 1),
        settings={
            'theme': 'dark',
            'notifications': True
        }
    )
    
    print("\n=== Serialization Options ===")
    print("Default serialization:")
    print(user.model_dump_json())
    
    print("\nSerialization with aliases:")
    print(user.model_dump_json(by_alias=True))
    
    print("\nExcluding fields:")
    print(user.model_dump_json(exclude={'settings', 'tags'}))
    
    print("\nIncluding specific fields:")
    print(user.model_dump_json(include={'username', 'status'}))


def demonstrate_nested_serialization():
    """Demonstrates serialization of nested structures."""
    class Address(BaseModel):
        street: str
        city: str
        country: str

    class Customer(BaseModel):
        name: str
        addresses: List[Address]
        metadata: Dict[str, Any]
        created_at: datetime

        model_config = ConfigDict(
            json_encoders={
                datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
            }
        )

    # Create nested structure
    customer = Customer(
        name="Alice",
        addresses=[
            Address(street="123 Main St", city="Boston", country="USA"),
            Address(street="456 Side St", city="New York", country="USA")
        ],
        metadata={
            "preferences": {"color": "blue"},
            "stats": {"visits": 10}
        },
        created_at=datetime.now()
    )
    
    rich.print("\n=== Nested Serialization ===")
    rich.print("Model:")
    rich.print(customer)
    
    rich.print("\nJSON:")
    rich.print(customer.model_dump_json(indent=2))


if __name__ == "__main__":
    demonstrate_basic_serialization()
    demonstrate_serialization_options()
    demonstrate_nested_serialization() 