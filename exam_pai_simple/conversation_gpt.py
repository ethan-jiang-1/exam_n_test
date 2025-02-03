"""Example of conversation with GPT model maintaining context."""
from pydantic_ai import Agent
from dotenv import load_dotenv

load_dotenv()

from exam_pai_simple.async_model import get_gpt_model

def run_gpt_conversation():
    """Demonstrate a contextual conversation using GPT model."""
    agent = Agent(  
        get_gpt_model(),
        defer_model_check=True,  
        system_prompt="you are helpful assistant, answer any user's question please. "
    )

    # First question about Einstein
    result1 = agent.run_sync('Who was Albert Einstein?')
    print("\nGPT Response 1:")
    print(result1.data)

    # Follow-up question using conversation history
    result2 = agent.run_sync(
        'What was his most famous equation?',
        message_history=result1.new_messages(),  
    )
    print("\nGPT Response 2:")
    print(result2.data)

if __name__ == "__main__":
    run_gpt_conversation() 