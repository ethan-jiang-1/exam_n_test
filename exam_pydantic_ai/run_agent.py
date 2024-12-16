from pydantic_ai import Agent
import rich
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

if __name__ == "__main__":
    result_sync_gpt = agent_gpt.run_sync('What is the capital of Italy?')
    rich.print(result_sync_gpt)
    print(result_sync_gpt.data)

    result_sync_qwen = agent_qwen.run_sync('What is the capital of Italy?')
    rich.print(result_sync_qwen)
    print(result_sync_qwen.data)
