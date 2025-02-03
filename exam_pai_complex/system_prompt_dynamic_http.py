import asyncio
from dataclasses import dataclass

import httpx
from dotenv import load_dotenv

from pydantic_ai import Agent, RunContext

load_dotenv()

from exam_pai_complex.async_model import get_gpt_model
model = get_gpt_model()


@dataclass
class MyDeps:
    api_key: str
    http_client: httpx.AsyncClient


agent = Agent(  
    model,
    defer_model_check=True,  
    deps_type=MyDeps 
)


@agent.system_prompt  
async def get_system_prompt(ctx: RunContext[MyDeps]) -> str:  
    response = await ctx.deps.http_client.get(  
        'https://example.com',
        headers={'Authorization': f'Bearer {ctx.deps.api_key}'},  
    )
    response.raise_for_status()
    return f'Prompt: {response.text}'


async def main():
    async with httpx.AsyncClient() as client:
        deps = MyDeps('foobar', client)
        result = await agent.run('Tell me a joke.', deps=deps)
        print(result.data)
        #> Did you hear about the toothpaste scandal? They called it Colgate.



if __name__ == "__main__":
    asyncio.run(main()) 