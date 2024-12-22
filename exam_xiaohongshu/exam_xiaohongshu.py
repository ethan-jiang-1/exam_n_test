import os
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

def get_azure_gpt_client():
    client = AzureOpenAI(api_key=os.getenv("OPENAI_API_KEY"),
                         azure_endpoint=os.getenv("OPENAI_BASE_URL"),
                         api_version=os.environ.get("AZURE_OPENAI_VERSION"))
    return client

def chat_gpt_plain(system_prompt=None, 
                   user_prompt=None):
    messages = [
        {"role": "system",
         "content": str(system_prompt)},
        {"role": "user",
         "content": str(user_prompt)}]
    client = get_azure_gpt_client()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages)
    return response.choices[0].message.content

system_prompt = "你很擅长写小红书的贴文，写作风格活波，容易吸引阅读"
user_prompt = "写一篇关于我最近使用的润唇膏，效果超级好，你想一下如何写出来吧，推荐的用户是中学生这个群体"
content = chat_gpt_plain(system_prompt=system_prompt, user_prompt=user_prompt)
print(content)