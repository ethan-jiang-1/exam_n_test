from flask import Flask
import httpx


app = Flask(__name__)

@app.route("/")
def hello():
    print("get called")
    return "Hello World!"

if __name__ == "__main__":
    transport = httpx.WSGITransport(app=app)
    with httpx.Client(transport=transport, base_url="http://testserver") as client:
        r = client.get("/")
        assert r.status_code == 200
        assert r.text == "Hello World!"