🔔 Webhook Handler

app/server/webhook_handler.py

`python
from fastapi import APIRouter, Request, Header
from app.server.verifysignature import verifysignature
from app.server.router import route_event
from app.utils.logger import logger

router = APIRouter()

@router.post("/webhook")
async def github_webhook(
    request: Request,
    xhubsignature_256: str | None = Header(None),
    xgithubevent: str | None = Header(None),
    xgithubdelivery: str | None = Header(None),
):
    raw_body = await request.body()

    if not verifysignature(rawbody, xhubsignature_256):
        logger.warn("Invalid signature", {"delivery": xgithubdelivery})
        return {"status": "invalid signature"}

    payload = await request.json()
    logger.info("Webhook received", {"event": xgithubevent})

    await routeevent(xgithub_event, payload)
    return {"status": "ok"}
