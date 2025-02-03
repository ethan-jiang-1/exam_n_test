"""Example of dependency injection in PydanticAI.
This example shows how to use dependencies that may not be used in every interaction.
"""
from dataclasses import dataclass
import asyncio
import httpx
from dotenv import load_dotenv
import logfire

from pydantic_ai import Agent

# Configure logging
logfire.configure(send_to_logfire='if-token-present')

load_dotenv()

from exam_pai_complex.async_model import get_gpt_model

@dataclass
class MyDeps:
    """Dependencies that may or may not be used in each interaction."""
    name: str  # User's name - will be used
    api_key: str  # API key - won't be used in this example
    http_client: httpx.AsyncClient  # HTTP client - won't be used in this example


agent = Agent(
    get_gpt_model(),
    defer_model_check=True,
    deps_type=MyDeps,
    system_prompt=(
        "You are a friendly assistant. If the user asks for a joke, "
        "tell a short, family-friendly joke. Always address the user by their name, "
        "which you can find in the context as 'name'."
    )
)


async def main():
    """Run the example showing unused dependencies."""
    async with httpx.AsyncClient() as client:
        # Create dependencies - only name will be used
        deps = MyDeps(
            name="Alice",  # This will be used
            api_key="unused_key",  # This won't be used
            http_client=client,  # This won't be used
        )
        
        # First interaction - using the name
        result1 = await agent.run(
            "Tell me a joke.",
            deps=deps,
        )
        print("\nFirst interaction (joke):")
        print(result1.data)

        # Second interaction - still using the name
        result2 = await agent.run(
            "Tell me another joke, but make it about programming.",
            deps=deps,
        )
        print("\nSecond interaction (programming joke):")
        print(result2.data)


if __name__ == "__main__":
    asyncio.run(main())