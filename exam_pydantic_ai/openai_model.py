import sys 
import os
import traceback
import httpx
import openai
import json
from pydantic_ai.models.openai import OpenAIModel
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table

load_dotenv()

if "./" not in sys.path:
    sys.path.append("./")

# 创建一个富文本控制台对象
console = Console()


async def log_response(response: httpx.Response):
    try:
        # Request Details
        request = response.request
        console.print("Request Details")
        table = Table(title="Request")
        table.add_column("Header", style="green", ratio=3)
        table.add_column("Value", style="cyan", ratio=7)
        for key, value in request.headers.items():
            table.add_row(key, value)
        console.print(table)

    except Exception:
        print("Error occurred in request handling:")
        print(traceback.format_exc())

    try:
        # Response Details
        console.print("\nResponse Details")
        table = Table(title="Response")
        table.add_column("Status Code", style="cyan")
        table.add_column("Headers", style="green")
        status_code = f"{response.status_code}"

        # Read the content asynchronously
        body = await response.aread()  # Read the full body content as bytes
        body_text = body.decode()  # Decode bytes into text

        # Prepare response headers to display in table
        headers = json.dumps(dict(response.headers), indent=2)
        table.add_row(status_code, headers)  # Don't include body in the table

        # Print the response table
        console.print(table)

        # Now print the response body separately
        console.print("\nResponse Body:\n", style="yellow")
        console.print(body_text)

        # Formatted JSON body: pretty-print formatted version of the body if it's JSON
        try:
            body_json = json.loads(body_text)  # Try parsing body as JSON
            formatted_body = json.dumps(body_json, indent=4)  # Indent for better readability
            console.print("\nFormatted JSON Response Body:\n", style="yellow")
            console.print(formatted_body)  # Print nicely formatted JSON
        except json.JSONDecodeError:
            # If it's not JSON, just print the raw body (already printed above)
            console.print("\nResponse Body is not a valid JSON format. Showing the raw version.")


    except Exception:
        print("Error occurred in response handling:")
        print(traceback.format_exc())



def get_model():
    # Initialize the Azure OpenAI client
    client = openai.AsyncAzureOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_BASE_URL"),
        api_version=os.getenv("AZURE_OPENAI_VERSION"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        http_client=httpx.AsyncClient(
            event_hooks={
                "response": [log_response]
            })
    )

    # Initialize the PydanticAI model with the Azure OpenAI client
    model = OpenAIModel('gpt-4o', openai_client=client)
    return model