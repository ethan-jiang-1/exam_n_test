import sys
import httpx 
import asyncio
import rich 

sys.path.append("./")

from starlette.applications import Starlette
from starlette.responses import HTMLResponse
from starlette.routing import Route


async def hello(request):
    return HTMLResponse("Hello World!")


app = Starlette(routes=[Route("/", hello)])

async def test():
    #from exam_httpx.asgi_app import app 
    transport = httpx.ASGITransport(app=app)

    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        r = await client.get("/")
        rich.print(r)
        rich.print(r.content)
        assert r.status_code == 200
        assert r.text == "Hello World!"


if __name__ == "__main__":
    asyncio.run(test())
    print("done")
