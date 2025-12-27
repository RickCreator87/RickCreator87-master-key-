from fastapi import FastAPI, Request, Header
import hmac, hashlib, os

app = FastAPI()

def verify_signature(secret, payload, signature):
    digest = "sha256=" + hmac.new(
        secret.encode(), payload, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(digest, signature)

@app.post("/github/webhook")
async def webhook(request: Request, xhubsignature256: str = Header(None), xgithub_event: str = Header(None)):
    body = await request.body()
    secret = os.getenv("GITHUBWEBHOOKSECRET")

    if not verifysignature(secret, body, xhubsignature256):
        return {"error": "Invalid signature"}

    if xgithubevent == "pull_request":
        return {"status": "PR logic"}
    return {"status": "OK"}
