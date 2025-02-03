from dataclasses import dataclass
import asyncio
import httpx
from dotenv import load_dotenv

from pydantic_ai import Agent

load_dotenv()

from exam_pai_complex.async_model import get_gpt_model
model_gpt = get_gpt_model()


@dataclass
class MyDeps:  
    api_key: str
    http_client: httpx.AsyncClient


# agent = Agent(
#     'openai:gpt-4o',
#     deps_type=MyDeps,  
# )

agent = Agent(  
    model_gpt,
    defer_model_check=True,  
    deps_type=MyDeps,  
    system_prompt="Use the customer's name while replying to them.",  
)


async def main():
    async with httpx.AsyncClient() as client:
        deps = MyDeps('foobar', client)
        result = await agent.run(
            'Tell me a joke.',
            deps=deps,  
        )
        print(result.data)
        #> Did you hear about the toothpaste scandal? They called it Colgate.

if __name__ == "__main__":
    asyncio.run(main())