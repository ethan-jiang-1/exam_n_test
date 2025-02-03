"""Generate Mermaid diagram for the question graph structure."""
from pathlib import Path
from question_graph_base import Ask, question_graph

def generate_mermaid(output_file: Path | None = None) -> None:
    """Generate a Mermaid diagram of the question graph.
    
    Args:
        output_file: Optional file path to save the diagram. If None, prints to stdout.
    """
    mermaid_code = question_graph.mermaid_code(start_node=Ask)
    
    if output_file:
        output_file.write_text(mermaid_code)
        print(f"Mermaid diagram saved to {output_file}")
    else:
        print(mermaid_code)

def main() -> None:
    """Main entry point for Mermaid diagram generation."""
    import sys
    
    if len(sys.argv) > 1:
        output_file = Path(sys.argv[1])
        generate_mermaid(output_file)
    else:
        generate_mermaid()

if __name__ == '__main__':
    main() 