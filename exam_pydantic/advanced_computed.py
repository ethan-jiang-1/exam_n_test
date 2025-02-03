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
from pydantic import BaseModel, Field, computed_field, field_validator, model_validator
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


class PriceCalculator(BaseModel):
    """
    Price calculator demonstrating field validators with dependencies.
    
    Attributes:
        base_price: Base price of the item
        quantity: Number of items
        discount_percent: Optional discount percentage
        tax_rate: Tax rate percentage
        is_wholesale: Whether this is a wholesale order
    """
    base_price: float = Field(gt=0)
    quantity: int = Field(gt=0)
    discount_percent: Optional[float] = Field(None, ge=0, le=100)
    tax_rate: float = Field(ge=0, le=100)
    is_wholesale: bool = False
    
    @field_validator('discount_percent')
    @classmethod
    def validate_discount(cls, v: Optional[float], info) -> Optional[float]:
        """Validate discount based on quantity."""
        if v is None:
            return v
            
        quantity = info.data.get('quantity', 0)
        is_wholesale = info.data.get('is_wholesale', False)
        
        # Maximum discount rules
        if is_wholesale and v > 40:
            raise ValueError("Wholesale discount cannot exceed 40%")
        elif not is_wholesale and v > 25:
            raise ValueError("Retail discount cannot exceed 25%")
            
        # Minimum quantity for discount
        if quantity < 5 and v > 10:
            raise ValueError("Orders less than 5 items cannot have discount > 10%")
            
        return v
    
    @model_validator(mode='after')
    def validate_total_price(self) -> 'PriceCalculator':
        """Validate the final price is not below minimum threshold."""
        total = self.total_price
        if total < 0:
            raise ValueError("Total price cannot be negative")
        
        min_price = 5.0 if not self.is_wholesale else 100.0
        if total < min_price:
            raise ValueError(f"Total price cannot be less than ${min_price}")
            
        return self
    
    @computed_field
    @property
    def subtotal(self) -> float:
        """Calculate subtotal before tax and discount."""
        return self.base_price * self.quantity
    
    @computed_field
    @property
    def discount_amount(self) -> float:
        """Calculate discount amount."""
        if not self.discount_percent:
            return 0.0
        return self.subtotal * (self.discount_percent / 100)
    
    @computed_field
    @property
    def tax_amount(self) -> float:
        """Calculate tax amount (applied after discount)."""
        return (self.subtotal - self.discount_amount) * (self.tax_rate / 100)
    
    @computed_field
    @property
    def total_price(self) -> float:
        """Calculate final price including discount and tax."""
        return self.subtotal - self.discount_amount + self.tax_amount


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
    
    # Price calculator example
    print("\n=== Price Calculations ===")
    
    # Retail order example
    try:
        retail_calc = PriceCalculator(
            base_price=29.99,
            quantity=3,
            discount_percent=10,
            tax_rate=8.5,
            is_wholesale=False
        )
        print("Retail Order:")
        print(f"Subtotal: ${retail_calc.subtotal:.2f}")
        print(f"Discount: ${retail_calc.discount_amount:.2f}")
        print(f"Tax: ${retail_calc.tax_amount:.2f}")
        print(f"Total: ${retail_calc.total_price:.2f}")
    except ValueError as e:
        print(f"Retail validation error: {e}")
    
    # Wholesale order example
    try:
        wholesale_calc = PriceCalculator(
            base_price=19.99,
            quantity=50,
            discount_percent=35,
            tax_rate=8.5,
            is_wholesale=True
        )
        print("\nWholesale Order:")
        print(f"Subtotal: ${wholesale_calc.subtotal:.2f}")
        print(f"Discount: ${wholesale_calc.discount_amount:.2f}")
        print(f"Tax: ${wholesale_calc.tax_amount:.2f}")
        print(f"Total: ${wholesale_calc.total_price:.2f}")
    except ValueError as e:
        print(f"Wholesale validation error: {e}")
    
    # Invalid discount example
    try:
        PriceCalculator(
            base_price=10.0,
            quantity=2,
            discount_percent=30,  # This should fail validation
            tax_rate=8.5,
            is_wholesale=False
        )
    except ValueError as e:
        print(f"\nValidation error (as expected): {e}")


if __name__ == "__main__":
    demonstrate_computed_fields() 