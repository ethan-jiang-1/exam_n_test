import asyncio
import logfire
from devtools import debug
from pydantic_graph import End

from question_graph_base import QuestionState, Answer, question_graph

async def run_continuous():
    """Run the question graph in continuous mode, asking questions until correct answer."""
    state = QuestionState()
    node = question_graph.start_node()
    history = []
    
    with logfire.span('run continuous questions'):
        try:
            while True:
                node = await question_graph.next(node, history, state=state)
                if isinstance(node, End):
                    debug([e.data_snapshot() for e in history])
                    break
                elif isinstance(node, Answer):
                    assert state.question, "Question must be set before answer"
                    try:
                        node.answer = input(f'{state.question} ')
                    except KeyboardInterrupt:
                        print("\nExiting...")
                        break
        except Exception as e:
            print(f"Error occurred: {e}")
            raise

if __name__ == '__main__':
    try:
        asyncio.run(run_continuous())
    except KeyboardInterrupt:
        print("\nExiting...") 