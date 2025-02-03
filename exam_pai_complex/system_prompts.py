from datetime import date

from pydantic_ai import Agent, RunContext
import sys 

if "./" not in sys.path:
    sys.path.append("./")

from exam_pydantic_ai.async_model import get_gpt_model
model_gpt = get_gpt_model()

agent = Agent(  
    model_gpt,
    defer_model_check=True,  
    deps_type=str,  
    system_prompt="Use the customer's name while replying to them.",  
)


@agent.system_prompt  
def add_the_users_name(ctx: RunContext[str]) -> str:
    return f"The user's name is {ctx.deps}."


@agent.system_prompt
def add_the_date() -> str:  
    return f'The date is {date.today()}.'


result = agent.run_sync('What is the date?', deps='Frank')
print(result.data)
#> Hello Frank, the date today is 2032-01-02.