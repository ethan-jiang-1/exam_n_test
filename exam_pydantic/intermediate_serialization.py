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
    """Demonstrates basic serialization features."""
    model = CustomSerializationModel(
        created_at=datetime.now(),
        updated_at=datetime.now(),
        data={'key': 'value', 'number': 42}
    )
    
    rich.print("\n=== Basic Serialization ===")
    rich.print("Model:", model)
    rich.print("JSON:", model.model_dump_json())
    rich.print("Dict:", model.model_dump())


def demonstrate_serialization_options():
    """Demonstrates various serialization options."""
    user = UserProfile(
        username="john_doe",
        status=UserStatus.ACTIVE,
        tags=["premium", "verified"],
        last_login=date.today(),
        settings={"theme": "dark", "notifications": True}
    )
    
    rich.print("\n=== Serialization Options ===")
    
    # Default serialization
    rich.print("\nDefault:")
    rich.print(user.model_dump())
    
    # Using aliases
    rich.print("\nWith aliases:")
    rich.print(user.model_dump(by_alias=True))
    
    # Excluding fields
    rich.print("\nExcluding fields:")
    rich.print(user.model_dump(exclude={'settings', 'tags'}))
    
    # Including specific fields
    rich.print("\nIncluding specific fields:")
    rich.print(user.model_dump(include={'username', 'status'}))


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