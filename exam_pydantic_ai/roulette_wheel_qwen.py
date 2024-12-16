from pydantic_ai import Agent, RunContext
import rich
import sys 

if "./" not in sys.path:
    sys.path.append("./")

from exam_pydantic_ai.async_model import get_qwen_model

roulette_agent = Agent(  
    get_qwen_model(),
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

    #result = roulette_agent.run_sync('Put my money on square eighteen', deps=success_number)
    #rich.print(result)

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

