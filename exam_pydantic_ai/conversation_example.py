from pydantic_ai import Agent
#import rich
import sys 

if "./" not in sys.path:
    sys.path.append("./")

from exam_pydantic_ai.async_model import get_gpt_model, get_qwen_model
model_gpt = get_gpt_model()
model_qwen = get_qwen_model()

agent_gpt = Agent(  
    model_gpt,
    defer_model_check=True,  
    system_prompt="you are helpful assistant, answer any user's question please. "
)

agent_qwen = Agent(  
    model_qwen,
    defer_model_check=True,  
    system_prompt="you are helpful assistant, answer any user's question please. "
)


def do_conversation(agent):
    # First run
    result1 = agent.run_sync('Who was Albert Einstein?')
    print(result1.data)
    #> Albert Einstein was a German-born theoretical physicist.

    # Second run, passing previous messages
    result2 = agent.run_sync(
        'What was his most famous equation?',
        message_history=result1.new_messages(),  
    )
    print(result2.data)
    #> Albert Einstein's most famous equation is (E = mc^2).


if __name__ == "__main__":
    do_conversation(agent_gpt)

    do_conversation(agent_qwen)
