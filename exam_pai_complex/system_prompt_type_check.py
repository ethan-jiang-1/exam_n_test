from dataclasses import dataclass

from pydantic_ai import Agent, RunContext
from dotenv import load_dotenv

load_dotenv()

from exam_pai_complex.async_model import get_gpt_model

model_gpt = get_gpt_model()

@dataclass
class User:
    name: str


agent = Agent(
    model_gpt,
    deps_type=User,  
    result_type=bool,
)


@agent.system_prompt
def add_user_name(ctx: RunContext[str]) -> str:  
    return f"The user's name is {ctx.deps}."


def foobar(x: bytes) -> None:
    pass


if __name__ == "__main__":
    result = agent.run_sync('Does their name start with "A"?', deps=User('Anne'))
    foobar(result.data) 