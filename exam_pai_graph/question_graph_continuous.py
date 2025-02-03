import asyncio
import logfire
import signal
import sys
from devtools import debug
from pydantic_graph import End

from question_graph_base import QuestionState, Answer, Ask, question_graph

# Global flag for graceful shutdown
shutdown_flag = False

def handle_interrupt(signum, frame):
    """Handle interrupt signal gracefully."""
    global shutdown_flag
    if not shutdown_flag:
        print("\nInitiating graceful shutdown... Press Ctrl+C again to force exit.")
        shutdown_flag = True
    else:
        print("\nForce exiting...")
        sys.exit(1)

async def run_continuous():
    """Run the question graph in continuous mode, asking questions until correct answer."""
    state = QuestionState()
    node = Ask()
    history = []
    
    with logfire.span('run continuous questions'):
        try:
            while not shutdown_flag:
                node = await question_graph.next(node, history, state=state)
                if isinstance(node, End):
                    debug([e.data_snapshot() for e in history])
                    print("Session completed successfully!")
                    break
                elif isinstance(node, Answer):
                    assert state.question, "Question must be set before answer"
                    try:
                        node.answer = input(f'{state.question} ')
                        if not node.answer.strip():
                            print("Please provide a non-empty answer.")
                            continue
                    except (KeyboardInterrupt, EOFError):
                        break
        except Exception as e:
            print(f"Error occurred: {e}")
            raise
        finally:
            if shutdown_flag:
                print("\nSession ended by user.")

def main() -> None:
    """Main entry point for continuous mode."""
    # Set up signal handlers
    signal.signal(signal.SIGINT, handle_interrupt)
    
    try:
        asyncio.run(run_continuous())
    except KeyboardInterrupt:
        pass  # Already handled by signal handler
    except Exception as e:
        print(f"Fatal error: {e}")
        raise
    finally:
        # Clean up any resources if needed
        pass

if __name__ == '__main__':
    main() 