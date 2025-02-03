"""Example of using static system prompts with decorators."""

from datetime import date

from pydantic_ai import Agent, RunContext
from dotenv import load_dotenv

load_dotenv()

from exam_pai_complex.async_model import get_gpt_model

model_gpt = get_gpt_model()

agent = Agent(  
    model_gpt,
    defer_model_check=True,  
    deps_type=str,  
    system_prompt="Use the customer's name while replying to them.",  
)


@agent.system_prompt  
def add_the_users_name(ctx: RunContext[str]) -> str:
    """Add user's name to system prompt."""
    return f"The user's name is {ctx.deps}."


@agent.system_prompt
def add_the_date() -> str:  
    """Add current date to system prompt."""
    return f'The date is {date.today()}.'


if __name__ == "__main__":
    result = agent.run_sync('What is the date?', deps='Frank')
    print("\nGPT Response:")
    print(result.data)