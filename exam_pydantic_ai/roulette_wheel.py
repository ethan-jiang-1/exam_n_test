from pydantic_ai import Agent, RunContext
import rich

def get_model():
    import os
    import openai
    from pydantic_ai.models.openai import OpenAIModel
    from dotenv import load_dotenv
    load_dotenv()

    # Initialize the Azure OpenAI client
    client = openai.AsyncAzureOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_BASE_URL"),
        api_version=os.getenv("AZURE_OPENAI_VERSION"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    )

    # Initialize the PydanticAI model with the Azure OpenAI client
    model = OpenAIModel('gpt-4o', openai_client=client)
    return model

roulette_agent = Agent(  
    get_model(),
    defer_model_check=True,  
    deps_type=int,
    result_type=bool,
    system_prompt=(
        'Use the `roulette_wheel` function to see if the '
        'customer has won based on the number they provide.'
    ),
)


@roulette_agent.tool
async def roulette_wheel(ctx: RunContext[int], square: int) -> str:  
    """check if the square is a winner"""
    ret = 'winner' if square == ctx.deps else 'loser'
    print(ret)
    return ret

def test1():
    # Run the agent
    success_number = 18  

    result = roulette_agent.run_sync('Put my money on square eighteen', deps=success_number)
    rich.print(result)

def test2():
    # Run the agent
    success_number = 18  

    result = roulette_agent.run_sync('I bet five is the winner', deps=success_number)
    rich.print(result)


if __name__ == "__main__":
    test1()
    #test2()

