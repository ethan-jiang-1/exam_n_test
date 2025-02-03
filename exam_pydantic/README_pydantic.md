# Pydantic Examples

This directory contains a comprehensive set of examples designed to help you understand and master the Pydantic library, which is used for data validation and settings management in Python using type annotations.

## Learning Structure Philosophy

This project is organized as a learning-focused structure rather than a production-oriented one. Each file is designed to be:

1. **Self-Contained Learning Unit**:
   - Complete documentation explaining concepts
   - Working examples that demonstrate features
   - Both successful and error cases
   - Runnable demonstrations

2. **Direct Learning Experience**:
   - Code serves as documentation
   - Running examples show immediate results
   - Comments explain concepts
   - Error handling is part of the learning

3. **Easy to Experiment**:
   - Modify code to see effects
   - Add your own test scenarios
   - Focus on understanding concepts
   - No separate test maintenance needed

## Directory Structure

### Basics (基础概念)
- **basics_model.py**: Basic model definition and usage
  - Creating simple models
  - Field type annotations
  - Basic model operations
- **basics_validation.py**: Basic field validation
  - Required vs optional fields
  - Field constraints
  - Error handling
- **basics_types.py**: Basic type system usage
  - Built-in types
  - Collection types
  - Optional and Union types

### Intermediate (中级特性)
- **intermediate_nested.py**: Nested model handling
  - Model composition
  - List and Dict of models
  - Recursive models
- **intermediate_validators.py**: Custom validators
  - Field validators
  - Model validators
  - Pre/post validation hooks
- **intermediate_config.py**: Model configuration
  - Model Config options
  - Custom config settings
  - Validation customization
- **intermediate_serialization.py**: Serialization and deserialization
  - JSON handling
  - Custom serialization
  - Export formats

### Advanced (高级功能)
- **advanced_computed.py**: Computed fields
  - Computed field properties
  - Dynamic field values
  - Dependencies between fields
- **advanced_generics.py**: Generic models
  - Type variables
  - Generic model inheritance
  - Parametrized types
- **advanced_rootmodel.py**: RootModel usage (V2)
  - List and Dict root types
  - Custom root types
  - Root validation
- **advanced_typeadapter.py**: TypeAdapter applications
  - Standalone type validation
  - Schema generation
  - Performance optimization
- **advanced_validators.py**: Advanced validation techniques
  - Wrap validators
  - Mode-specific validation
  - Complex validation chains
  - Context-aware validation

### Practical (实际应用)
- **practical_settings.py**: Configuration management
  - Environment variables
  - Nested settings
  - Dynamic settings
- **practical_api.py**: API data validation
  - Request/Response models
  - FastAPI integration
  - OpenAPI schema generation
- **practical_orm.py**: ORM integration
  - SQLAlchemy models
  - Data conversion
  - Validation layers
- **practical_migration.py**: V1 to V2 migration
  - Breaking changes
  - Migration strategies
  - Compatibility handling

### Performance (性能优化)
- **performance_benchmark.py**: Performance testing
  - Validation benchmarks
  - Memory usage
  - Optimization metrics
- **performance_optimize.py**: Optimization techniques
  - Model design optimization
  - Validation optimization
  - Memory optimization

## File Structure

Each example file follows this structure:
```python
"""
Detailed module documentation explaining:
- What you will learn
- Key concepts covered
- How to use the examples
"""

# Imports and setup

class ExampleModel(BaseModel):
    """
    Detailed class documentation with:
    - Purpose
    - Attributes
    - Usage examples
    """
    field: type

def demonstrate_feature():
    """
    Function demonstrating specific features with:
    - Purpose
    - Example usage
    - Expected results
    """
    # Implementation with comments
    # Both success and error cases

if __name__ == "__main__":
    # Direct demonstration when running the file
    demonstrate_feature()

## Key Concepts

1. **Model Definition**: Learn how to define data models using Pydantic's `BaseModel` and type annotations.
2. **Data Validation**: Understand automatic data validation against model schemas.
3. **Error Handling**: Master error catching and interpretation.
4. **Serialization**: Utilize model serialization and deserialization features.

## Getting Started

1. Start with the basics examples to understand core concepts
2. Progress through intermediate examples for more complex scenarios
3. Explore advanced examples for deeper understanding
4. Study practical examples for real-world applications
5. Consider performance examples for optimization needs

## Running Examples

Each example file can be run independently:
```bash
python basics_model.py
```

The output will show:
- Example model usage
- Validation in action
- Error handling cases
- Different scenarios

## Version Compatibility

These examples are compatible with Pydantic V2. For V1 compatibility, check the migration examples in the advanced section.

## Contributing

When adding new examples:
1. Follow the naming convention (basics_, intermediate_, etc.)
2. Include comprehensive comments and docstrings
3. Make sure examples are self-contained and runnable
4. Update this README with new example descriptions 