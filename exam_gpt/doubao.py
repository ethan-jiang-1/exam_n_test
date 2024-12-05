'''
Usage:

1. python3 -m pip install --user volcengine
2. VOLC_ACCESSKEY=XXXXX VOLC_SECRETKEY=YYYYY python main.py
'''


import os
from dotenv import load_dotenv
load_dotenv

from volcengine.maas.v2 import MaasService
from volcengine.maas import MaasException, ChatRole

def test_chat(maas, endpoint_id, req):
    try:
        resp = maas.chat(endpoint_id, req)
        print(resp)
    except MaasException as e:
        print(e)

def test_stream_chat(maas, endpoint_id, req):
    try:
        resps = maas.stream_chat(endpoint_id, req)
        for resp in resps:
            print(resp)
    except MaasException as e:
        print(e)

if __name__ == '__main__':
    maas = MaasService('maas-api.ml-platform-cn-beijing.volces.com', 'cn-beijing')

    maas.set_ak(os.getenv("VOLC_ACCESSKEY"))
    maas.set_sk(os.getenv("VOLC_SECRETKEY"))

    # document: "https://www.volcengine.com/docs/82379/1099475"
    # chat
    req = {
        
        "messages": [
            {
                "role": ChatRole.USER,
                "content": "天为什么这么蓝"
            }, {
                "role": ChatRole.ASSISTANT,
                "content": "因为有你"
            }, {
                "role": ChatRole.USER,
                "content": "花儿为什么这么香？"
            },
        ]
    }

    endpoint_id = os.getenv("YOUR_ENDPOINT_ID") # "{YOUR_ENDPOINT_ID}"
    test_chat(maas, endpoint_id, req)
    test_stream_chat(maas, endpoint_id, req)
#