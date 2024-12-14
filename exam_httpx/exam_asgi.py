import sys 

sys.path.append("./")


from exam_httpx.asgi_app import app 

if __name__ == "__main__":
    transport = httpx.ASGITransport(app=app)

    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        r = await client.get("/")
        assert r.status_code == 200
        assert r.text == "Hello World!"