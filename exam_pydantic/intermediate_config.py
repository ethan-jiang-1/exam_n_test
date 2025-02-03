"""
Intermediate Pydantic Configuration Examples
=========================================

This module demonstrates various configuration options in Pydantic, including:
1. Model configuration
2. Schema customization
3. Field aliases
4. Custom JSON encoders
5. Model documentation

Key concepts covered:
- ConfigDict usage
- JSON Schema generation
- Field customization
- Documentation generation
"""

from enum import Enum
from typing import Optional
from typing_extensions import Annotated
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
import rich
import json


class Gender(str, Enum):
    """
    Enumeration of gender options.
    
    Values:
        male: Male gender
        female: Female gender
        other: Other gender options
        not_given: Prefer not to specify
    """
    male = 'male'
    female = 'female'
    other = 'other'
    not_given = 'not_given'


class UserMetadata(BaseModel):
    """
    User metadata information.
    
    Attributes:
        last_login: Last login timestamp
        login_count: Number of times logged in
        is_active: Whether the user is active
    """
    last_login: datetime | None = None
    login_count: int = 0
    is_active: bool = True


class UserProfile(BaseModel):
    """
    Main user profile model with custom configuration.
    
    This model demonstrates various configuration options and schema customization.
    """
    model_config = ConfigDict(
        title='User Profile Schema',
        description='A comprehensive user profile with metadata',
        json_schema_extra={
            'examples': [
                {
                    'username': 'john_doe',
                    'gender': 'male',
                    'age': 30,
                    'metadata': {
                        'login_count': 10,
                        'is_active': True
                    }
                }
            ]
        }
    )

    username: str = Field(
        title='Username',
        description='Unique username for the user',
        min_length=3,
        max_length=50
    )
    gender: Annotated[
        Optional[Gender],
        Field(title='Gender', description='User\'s gender identity')
    ] = None
    age: Annotated[
        Optional[int],
        Field(
            title='Age',
            description='User\'s age in years',
            ge=0,
            le=150
        )
    ] = None
    metadata: UserMetadata = Field(
        default_factory=UserMetadata,
        title='User Metadata',
        description='Additional user information'
    )


def demonstrate_schema_generation():
    """Demonstrates JSON schema generation and customization."""
    # Generate JSON schema
    schema = UserProfile.model_json_schema()
    
    rich.print("\n=== JSON Schema ===")
    rich.print(json.dumps(schema, indent=2))
    
    # Show schema properties
    rich.print("\n=== Schema Properties ===")
    for prop, details in schema.get('properties', {}).items():
        rich.print(f"\nProperty: {prop}")
        rich.print(f"Title: {details.get('title')}")
        rich.print(f"Description: {details.get('description')}")
        if 'minimum' in details:
            rich.print(f"Minimum: {details['minimum']}")
        if 'maximum' in details:
            rich.print(f"Maximum: {details['maximum']}")


def demonstrate_model_usage():
    """Demonstrates model instantiation and validation."""
    # Create a user with all fields
    user1 = UserProfile(
        username="jane_doe",
        gender=Gender.female,
        age=25,
        metadata=UserMetadata(
            last_login=datetime.now(),
            login_count=5,
            is_active=True
        )
    )
    
    rich.print("\n=== Complete User Profile ===")
    rich.print(user1.model_dump())
    
    # Create a user with minimal fields
    user2 = UserProfile(username="john_doe")
    rich.print("\n=== Minimal User Profile ===")
    rich.print(user2.model_dump())


def demonstrate_json_handling():
    """Demonstrates JSON serialization and deserialization."""
    user = UserProfile(
        username="test_user",
        gender=Gender.other,
        age=30,
        metadata=UserMetadata(
            last_login=datetime.now(),
            login_count=1
        )
    )
    
    # Serialize to JSON
    json_data = user.model_dump_json()
    rich.print("\n=== Serialized to JSON ===")
    rich.print(json_data)
    
    # Deserialize from JSON
    deserialized = UserProfile.model_validate_json(json_data)
    rich.print("\n=== Deserialized from JSON ===")
    rich.print(deserialized)


if __name__ == "__main__":
    demonstrate_schema_generation()
    demonstrate_model_usage()
    demonstrate_json_handling() 