👥 Onboarding — app/logic/onboarding.py

`python
from app.ai.modelrouter import routeto_model

async def handle_installation(payload: dict):
    account = payload["installation"]["account"]["login"]
    return await routetomodel("onboarding", text=f"New installation: {account}")
