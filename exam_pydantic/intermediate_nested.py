"""
Intermediate Pydantic Nested Model Examples
=======================================

This module demonstrates advanced nested model patterns in Pydantic, including:
1. Model composition
2. Recursive models
3. Complex data structures
4. Forward references
5. Circular dependencies

Key concepts covered:
- Nested model relationships
- Self-referential models
- Collection of models
- Model dependencies
"""

from typing import Dict, List, Optional, Set, Union
from pydantic import BaseModel
import rich


class Comment(BaseModel):
    """
    A comment model that can have nested replies.
    
    Attributes:
        content: The comment text
        author: Author's name
        replies: List of nested reply comments
        likes: Number of likes
    """
    content: str
    author: str
    replies: List['Comment'] = []  # Self-referential
    likes: int = 0


# Required for self-referential models
Comment.model_rebuild()


class Address(BaseModel):
    """
    Address information.
    
    Attributes:
        street: Street name
        city: City name
        country: Country name
        is_primary: Whether this is the primary address
    """
    street: str
    city: str
    country: str
    is_primary: bool = False


class Department(BaseModel):
    """
    Department model with recursive employee structure.
    
    Attributes:
        name: Department name
        head: Lead employee
        employees: List of employees in the department
        sub_departments: Nested departments
    """
    name: str
    head: Optional['Employee'] = None
    employees: List['Employee'] = []
    sub_departments: List['Department'] = []


class Employee(BaseModel):
    """
    Employee model with complex relationships.
    
    Attributes:
        name: Employee name
        title: Job title
        department: Reference to department
        addresses: Multiple addresses
        manager: Optional manager reference
        subordinates: List of managed employees
        skills: Set of skills
        metadata: Additional data
    """
    name: str
    title: str
    department: Optional[Department] = None
    addresses: List[Address] = []
    manager: Optional['Employee'] = None
    subordinates: List['Employee'] = []
    skills: Set[str] = set()
    metadata: Dict[str, Union[str, int, float]] = {}


# Required for forward references
Employee.model_rebuild()
Department.model_rebuild()


def demonstrate_comment_thread():
    """Demonstrates nested comment structure."""
    # Create a comment thread
    comment = Comment(
        content="Great article!",
        author="John",
        replies=[
            Comment(
                content="Thanks!",
                author="Author",
                replies=[
                    Comment(
                        content="You're welcome!",
                        author="John",
                        likes=2
                    )
                ],
                likes=3
            ),
            Comment(
                content="Very informative",
                author="Alice",
                likes=1
            )
        ],
        likes=5
    )
    
    rich.print("\n=== Comment Thread ===")
    rich.print(comment.model_dump_json(indent=2))


def demonstrate_organization_structure():
    """Demonstrates complex organizational structure."""
    # Create organization structure
    tech_dept = Department(
        name="Technology",
        employees=[
            Employee(
                name="Alice Engineer",
                title="Software Engineer",
                addresses=[
                    Address(
                        street="123 Tech St",
                        city="San Francisco",
                        country="USA",
                        is_primary=True
                    )
                ],
                skills={"Python", "Pydantic", "FastAPI"},
                metadata={"years_experience": 5, "team": "Backend"}
            )
        ],
        sub_departments=[
            Department(
                name="Frontend",
                employees=[
                    Employee(
                        name="Bob Designer",
                        title="UI Developer",
                        skills={"JavaScript", "React"},
                        metadata={"years_experience": 3}
                    )
                ]
            )
        ]
    )
    
    rich.print("\n=== Organization Structure ===")
    rich.print(tech_dept.model_dump_json(indent=2))


def demonstrate_employee_relationships():
    """Demonstrates employee relationships and circular references."""
    # Create manager and subordinates
    manager = Employee(
        name="Team Lead",
        title="Engineering Manager",
        skills={"Leadership", "Architecture"},
        addresses=[
            Address(street="456 Lead St", city="Boston", country="USA", is_primary=True)
        ]
    )
    
    dev1 = Employee(
        name="Developer 1",
        title="Senior Developer",
        manager=manager,
        skills={"Python", "Databases"}
    )
    
    dev2 = Employee(
        name="Developer 2",
        title="Junior Developer",
        manager=manager,
        skills={"Python", "Testing"}
    )
    
    # Update manager with subordinates
    manager.subordinates = [dev1, dev2]
    
    rich.print("\n=== Employee Relationships ===")
    rich.print("Manager:", manager.name)
    rich.print("Subordinates:", [emp.name for emp in manager.subordinates])
    rich.print("Dev1's manager:", dev1.manager.name)


if __name__ == "__main__":
    demonstrate_comment_thread()
    demonstrate_organization_structure()
    demonstrate_employee_relationships() 