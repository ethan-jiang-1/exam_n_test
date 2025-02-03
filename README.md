# exam_n_test

This project serves as a host for various experimental files, each contained within its respective `exam_xxxx` subdirectory. The purpose of this repository is to provide a structured environment for testing and exploring different concepts and libraries in Python.

## Project Structure

- **exam_pydantic**: Contains examples and tests related to the Pydantic library, focusing on data validation and settings management.
- **exam_httpx**: Contains examples related to HTTPX for making HTTP requests.
- **exam_pydantic_ai**: Contains experiments related to AI models using Pydantic.
- **exam_funcall_simple**: Contains function calling examples and tests.

## Environment Setup

The project uses a root-level `.env` file for configuration:
1. All subprojects can access shared configuration (e.g., API keys) from the root `.env` file
2. The `.env` file includes PYTHONPATH settings that point to the project root directory
3. Simply use Python's environment loading (e.g., `python-dotenv`) in your code to access these settings

### PYTHONPATH Configuration
The `.env` file sets up PYTHONPATH to include the project root directory. This means:
- You can import modules from any subdirectory using the exam_xxxx package path
- For example, if you're in `exam_httpx` and want to use code from `exam_pydantic`:
  ```python
  from exam_pydantic.pydantic_schema import SomeModel
  ```
- No need to modify sys.path or create complex relative imports
- All imports will work consistently regardless of which directory you run from

Example of using environment variables in subprojects:
```python
from dotenv import load_dotenv
load_dotenv()  # This will automatically find and load the root .env file
```

## Getting Started

To get started with any of the experiments:
1. Navigate to the respective subdirectory
2. Read the README file within that directory for specific instructions
3. Follow the examples and run the tests to understand the concepts

## Contributing

When adding new experiments:
1. Create a new directory with the prefix `exam_`
2. Include a README file explaining the purpose and usage
3. Add well-documented code with appropriate tests
4. Update this root README.md to reflect the new addition
5. Use the shared `.env` configuration when needed

## Note

Each subdirectory is self-contained and focuses on specific aspects of Python libraries or concepts. Refer to individual README files within each directory for detailed information.

