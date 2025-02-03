# Pydantic AI Examples

## Overview
This directory contains examples demonstrating the usage of `pydantic_ai` library with different AI models (Azure OpenAI GPT and Alibaba Qwen). Each example is separated by model type for clarity and maintainability.

## Directory Structure
```
exam_pydantic_ai/
├── async_model.py              # Model configuration and HTTP client setup
├── conversation_gpt.py         # Conversation example with GPT
├── conversation_qwen.py        # Conversation example with Qwen
├── run_agent_gpt.py           # Basic agent example with GPT
├── run_agent_qwen.py          # Basic agent example with Qwen
├── roulette_wheel_gpt.py      # Game example with GPT
├── roulette_wheel_qwen.py     # Game example with Qwen
└── README.md                  # This documentation
```

## Core Components

### Model Configuration (`async_model.py`)
- Configures async HTTP clients for both models
- Implements detailed request/response logging
- Provides model factory functions:
  - `get_gpt_model()`: Azure OpenAI GPT configuration
  - `get_qwen_model()`: Alibaba Qwen configuration

### Basic Examples
Each example is implemented for both GPT and Qwen models:

#### Single Query Examples
- `run_agent_gpt.py`: Basic GPT query
- `run_agent_qwen.py`: Basic Qwen query
```python
# Example usage
result = agent.run_sync('What is the capital of Italy?')
```

#### Conversation Examples
- `conversation_gpt.py`: Multi-turn conversation with GPT
- `conversation_qwen.py`: Multi-turn conversation with Qwen
```python
# Example usage with history
result2 = agent.run_sync(
    'Follow-up question',
    message_history=result1.new_messages()
)
```

#### Game Examples
- `roulette_wheel_gpt.py`: Roulette game with GPT
- `roulette_wheel_qwen.py`: Roulette game with Qwen
```python
@roulette_agent.tool
async def roulette_wheel(ctx: RunContext[int], square: int) -> str:
    return 'winner' if square == ctx.deps else 'loser'
```

## Environment Setup

Required environment variables:
```env
# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=<endpoint>
AZURE_OPENAI_BASE_URL=<base-url>
AZURE_OPENAI_API_KEY=<api-key>
AZURE_OPENAI_VERSION=<version>

# Alibaba Qwen Configuration
DASHSCOPE_API_KEY=<api-key>
```

## Usage Examples

### Running GPT Examples
```bash
# Basic query
python run_agent_gpt.py

# Conversation
python conversation_gpt.py

# Roulette game
python roulette_wheel_gpt.py
```

### Running Qwen Examples
```bash
# Basic query
python run_agent_qwen.py

# Conversation
python conversation_qwen.py

# Roulette game
python roulette_wheel_qwen.py
```

## Key Features

1. **Model Separation**
   - Clear separation between GPT and Qwen implementations
   - Model-specific configurations and optimizations
   - Easy comparison between model behaviors

2. **Code Organization**
   - Each example has dedicated files for each model
   - Consistent file naming convention
   - Clear documentation and examples

3. **Logging and Debugging**
   - Rich console output
   - Detailed request/response logging
   - Error handling for each model

## Development Guidelines

1. **File Organization**
   - Keep GPT and Qwen implementations separate
   - Use consistent naming patterns
   - Maintain parallel structure between implementations

2. **Code Style**
   - Include docstrings and comments
   - Use type hints
   - Follow consistent formatting

3. **Testing**
   - Test each model implementation separately
   - Verify error handling
   - Check model-specific behaviors

## Troubleshooting

Common issues and solutions:
1. **GPT Issues**
   - Check Azure OpenAI configuration
   - Verify API version compatibility
   - Check rate limits

2. **Qwen Issues**
   - Verify Dashscope API key
   - Check endpoint availability
   - Monitor usage quotas

## Future Improvements
1. Add more complex examples
2. Implement comparative testing
3. Add performance benchmarks
4. Enhance error handling
5. Add more documentation 