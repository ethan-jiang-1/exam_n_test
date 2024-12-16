import sys 
import os
import traceback
import httpx
import json
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table

load_dotenv()

if "./" not in sys.path:
    sys.path.append("./")

# 创建一个富文本控制台对象
console = Console()

g_response_count = 0

async def log_response(response: httpx.Response):
    global g_response_count 

    print("\n\n--\n")
    try:
        # Request Details
        request = response.request
        console.print(f">> **{g_response_count:02}**  Request Details for request", style="blue")
        table = Table(title="Request")
        table.add_column("Header", style="green", ratio=3)
        table.add_column("Value", style="cyan", ratio=7)
        for key, value in request.headers.items():
            table.add_row(key, value)
        console.print(table)

        # Print Request Body
        if request.content:  # Check if there is a body in the request
            console.print("\nRequest Body:\n", style="yellow")
            request_body = request.content.decode() if isinstance(request.content, bytes) else str(request.content)
            # Try to parse and format the request body if it's JSON
            try:
                request_json = json.loads(request_body)
                formatted_request_body = json.dumps(request_json, indent=4)  # Indent for readability
                console.print("\nFormatted JSON Request Body:\n", style="yellow")
                console.print(formatted_request_body)
            except json.JSONDecodeError:
                # If it's not JSON, print the raw body
                console.print(request_body)
        else:
            console.print("\nNo Request Body.\n", style="yellow")

    except Exception:
        print("Error occurred in request handling:")
        print(traceback.format_exc())

    try:
        # Response Details
        console.print(f"\n<< **{g_response_count:02}** Response Details", style="blue")
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

    g_response_count += 1


def get_gpt_model():
    import openai
    from pydantic_ai.models.openai import OpenAIModel

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


def get_qwen_model():
    import openai
    from pydantic_ai.models.openai import OpenAIModel

    client = openai.AsyncOpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        http_client=httpx.AsyncClient(
            event_hooks={
                "response": [log_response]
            })
    )

    # Initialize the PydanticAI model with the Azure OpenAI client
    model_name = "qwen-plus-1127"
    #model_name = "qwen-max-latest"
    model = OpenAIModel(model_name, openai_client=client)
    return model

if __name__ == "__main__":
    model1 = get_gpt_model()
    console.print(model1)

    model2 = get_qwen_model()
    console.print(model2)