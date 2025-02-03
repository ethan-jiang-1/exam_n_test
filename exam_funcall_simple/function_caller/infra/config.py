import os
from dotenv import load_dotenv
from openai import AzureOpenAI

# Load environment variables from project root
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_VERSION = os.getenv("AZURE_OPENAI_VERSION", "2024-02-15-preview")

# Model Configuration
GPT4_DEPLOYMENT_NAME = "gpt-4o"

def test_azure_connection():
    """测试Azure OpenAI连接是否正常"""
    try:
        client = AzureOpenAI(
            api_key=AZURE_OPENAI_API_KEY,
            api_version=AZURE_OPENAI_VERSION,
            azure_endpoint=AZURE_OPENAI_ENDPOINT
        )
        
        # 发送一个简单的测试请求
        response = client.chat.completions.create(
            model=GPT4_DEPLOYMENT_NAME,
            messages=[
                {"role": "user", "content": "Say 'Hello, World!'"}
            ],
            max_tokens=30
        )
        
        return True, response.choices[0].message.content
    except Exception as e:
        return False, str(e)

if __name__ == "__main__":
    # 测试配置是否正确加载
    print("Azure OpenAI Endpoint:", AZURE_OPENAI_ENDPOINT)
    print("API Version:", AZURE_OPENAI_VERSION)
    print("Model Name:", GPT4_DEPLOYMENT_NAME)
    
    # 测试Azure连接
    print("\n=== Testing Azure OpenAI Connection ===")
    success, result = test_azure_connection()
    if success:
        print("✅ Connection successful!")
        print("Response:", result)
    else:
        print("❌ Connection failed!")
        print("Error:", result) 