import os
from dotenv import load_dotenv

# Load environment variables from project root
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_VERSION = os.getenv("AZURE_OPENAI_VERSION", "2024-02-15-preview")

# Model Configuration
GPT4_DEPLOYMENT_NAME = "gpt-4o"

if __name__ == "__main__":
    # 测试配置是否正确加载
    print("Azure OpenAI Endpoint:", AZURE_OPENAI_ENDPOINT)
    print("API Version:", AZURE_OPENAI_VERSION)
    print("Model Name:", GPT4_DEPLOYMENT_NAME) 