import asyncio
import sys
from pathlib import Path
import logfire
from devtools import debug
from pydantic_graph import End
from typing import Optional

from question_graph_base import QuestionState, Answer, question_graph

async def run_cli(answer: Optional[str] = None) -> None:
    """Run the question graph in CLI mode with history support.
    
    Args:
        answer: Optional answer to continue from previous state
    """
    history_file = Path('question_graph_history.json')
    history = []
    
    try:
        if history_file.exists():
            history = question_graph.load_history(history_file.read_bytes())
    except Exception as e:
        print(f"Error loading history: {e}")
        history = []

    with logfire.span('run cli questions'):
        try:
            if history:
                last = history[-1]
                assert last.kind == 'node', 'expected last step to be a node'
                state = last.state
                if answer is None:
                    print("Error: answer is required to continue from history")
                    return
                node = Answer(answer)
            else:
                state = QuestionState()
                node = question_graph.start_node()
            debug(state, node)

            while True:
                node = await question_graph.next(node, history, state=state)
                if isinstance(node, End):
                    debug([e.data_snapshot() for e in history])
                    print('Finished!')
                    break
                elif isinstance(node, Answer):
                    print(state.question)
                    break

            # Save history
            try:
                history_file.write_bytes(question_graph.dump_history(history, indent=2))
            except Exception as e:
                print(f"Error saving history: {e}")

        except Exception as e:
            print(f"Error occurred: {e}")
            raise

def main() -> None:
    """Main entry point for CLI mode."""
    if len(sys.argv) < 2:
        print("Usage: python question_graph_cli.py <answer>")
        print("  or: python question_graph_cli.py --new (to start new session)")
        sys.exit(1)

    answer = None if sys.argv[1] == '--new' else sys.argv[1]
    try:
        asyncio.run(run_cli(answer))
    except KeyboardInterrupt:
        print("\nExiting...")

if __name__ == '__main__':
    main() 