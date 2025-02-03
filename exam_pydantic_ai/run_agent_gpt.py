"""Basic example of running a GPT agent for a single query."""
from pydantic_ai import Agent
import rich
import sys 

if "./" not in sys.path:
    sys.path.append("./")

from exam_pydantic_ai.async_model import get_gpt_model

def run_gpt_query():
    """Run a simple query using GPT model."""
    agent = Agent(  
        get_gpt_model(),
        defer_model_check=True,  
        system_prompt="you are helpful assistant, answer any user's question please. "
    )

    # Run a simple query
    result = agent.run_sync('What is the capital of Italy?')
    print("\nGPT Response:")
    rich.print(result)
    print("\nGPT Answer:")
    print(result.data)

if __name__ == "__main__":
    run_gpt_query() 