"""
Advanced Pydantic Computed Fields Examples
=====================================

This module demonstrates advanced computed field patterns in Pydantic, including:
1. Computed fields using properties
2. Dynamic default values
3. Field validators with dependencies
4. Computed fields with caching
5. Model methods as computed values

Key concepts covered:
- Property-based computed fields
- Dependent field calculations
- Dynamic field updates
- Performance optimization
- Complex computed relationships
"""

from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from functools import cached_property
from pydantic import BaseModel, Field, computed_field
import math


class Circle(BaseModel):
    """
    Circle model demonstrating basic computed fields.
    
    Attributes:
        radius: Circle radius
        diameter: Computed diameter
        area: Computed area
        circumference: Computed circumference
    """
    radius: float = Field(gt=0, description="Circle radius (must be positive)")
    
    @computed_field
    @property
    def diameter(self) -> float:
        """Compute diameter from radius."""
        return self.radius * 2
    
    @computed_field
    @property
    def area(self) -> float:
        """Compute circle area."""
        return math.pi * self.radius ** 2
    
    @computed_field
    @property
    def circumference(self) -> float:
        """Compute circle circumference."""
        return 2 * math.pi * self.radius


class GradeBook(BaseModel):
    """
    Grade book demonstrating cached computed fields.
    
    Attributes:
        student_name: Name of the student
        grades: List of numeric grades
        weights: Optional weights for each grade
    """
    student_name: str
    grades: List[float] = Field(default_factory=list)
    weights: Optional[List[float]] = None
    
    @computed_field
    @cached_property
    def weighted_average(self) -> float:
        """
        Calculate weighted average of grades.
        Uses equal weights if no weights are specified.
        """
        if not self.grades:
            return 0.0
        
        if not self.weights:
            return sum(self.grades) / len(self.grades)
        
        if len(self.weights) != len(self.grades):
            raise ValueError("Number of weights must match number of grades")
        
        return sum(g * w for g, w in zip(self.grades, self.weights)) / sum(self.weights)
    
    @computed_field
    @property
    def letter_grade(self) -> str:
        """Convert numeric average to letter grade."""
        avg = self.weighted_average
        if avg >= 90:
            return 'A'
        elif avg >= 80:
            return 'B'
        elif avg >= 70:
            return 'C'
        elif avg >= 60:
            return 'D'
        else:
            return 'F'
    
    @computed_field
    @property
    def passing(self) -> bool:
        """Determine if the student is passing."""
        return self.weighted_average >= 60


class ExpenseTracker(BaseModel):
    """
    Expense tracker demonstrating dynamic computed fields.
    
    Attributes:
        expenses: List of expenses with amounts and categories
        budget: Monthly budget amount
        start_date: Start of tracking period
    """
    expenses: List[Dict[str, Any]] = Field(default_factory=list)
    budget: float = Field(gt=0)
    start_date: datetime = Field(default_factory=datetime.now)
    
    @computed_field
    @property
    def total_expenses(self) -> float:
        """Calculate total expenses."""
        return sum(expense['amount'] for expense in self.expenses)
    
    @computed_field
    @property
    def remaining_budget(self) -> float:
        """Calculate remaining budget."""
        return self.budget - self.total_expenses
    
    @computed_field
    @property
    def expense_by_category(self) -> Dict[str, float]:
        """Group expenses by category."""
        categories: Dict[str, float] = {}
        for expense in self.expenses:
            category = expense['category']
            amount = expense['amount']
            categories[category] = categories.get(category, 0) + amount
        return categories
    
    @computed_field
    @property
    def days_remaining(self) -> int:
        """Calculate days remaining in the current month."""
        now = datetime.now()
        next_month = (now.replace(day=1) + timedelta(days=32)).replace(day=1)
        return (next_month - now).days
    
    @computed_field
    @property
    def daily_budget_remaining(self) -> float:
        """Calculate remaining daily budget."""
        if self.days_remaining <= 0:
            return 0.0
        return self.remaining_budget / self.days_remaining


def demonstrate_computed_fields():
    """Demonstrate the usage of computed fields."""
    # Circle example
    circle = Circle(radius=5)
    print("=== Circle Computations ===")
    print(f"Circle with radius {circle.radius}:")
    print(f"Diameter: {circle.diameter:.2f}")
    print(f"Area: {circle.area:.2f}")
    print(f"Circumference: {circle.circumference:.2f}")
    
    # Grade book example
    gradebook = GradeBook(
        student_name="Alice Smith",
        grades=[85, 92, 78, 95, 88],
        weights=[0.1, 0.3, 0.2, 0.3, 0.1]
    )
    print("\n=== Grade Calculations ===")
    print(f"Student: {gradebook.student_name}")
    print(f"Weighted Average: {gradebook.weighted_average:.2f}")
    print(f"Letter Grade: {gradebook.letter_grade}")
    print(f"Passing: {gradebook.passing}")
    
    # Expense tracker example
    tracker = ExpenseTracker(
        budget=1000,
        expenses=[
            {"category": "Food", "amount": 250.50},
            {"category": "Transport", "amount": 120.75},
            {"category": "Food", "amount": 175.25},
            {"category": "Entertainment", "amount": 85.00}
        ]
    )
    print("\n=== Expense Tracking ===")
    print(f"Total Expenses: ${tracker.total_expenses:.2f}")
    print(f"Remaining Budget: ${tracker.remaining_budget:.2f}")
    print("Expenses by Category:")
    for category, amount in tracker.expense_by_category.items():
        print(f"  {category}: ${amount:.2f}")
    print(f"Days Remaining: {tracker.days_remaining}")
    print(f"Daily Budget Remaining: ${tracker.daily_budget_remaining:.2f}")


if __name__ == "__main__":
    demonstrate_computed_fields() 