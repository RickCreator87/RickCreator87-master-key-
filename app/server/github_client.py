🔑 GitHub App Authentication (JWT + Installation Token)

app/server/github_client.py

`python
import jwt
import time
import httpx
from app.utils.config import config

def generate_jwt():
    now = int(time.time())
    payload = {
        "iat": now - 60,
        "exp": now + (9 * 60),
        "iss": config.GITHUBAPPID,
    }

    privatekey = config.GITHUBPRIVATE_KEY
    return jwt.encode(payload, private_key, algorithm="RS256")

async def getinstallationclient(installation_id: int):
    token = generate_jwt()

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"https://api.github.com/app/installations/{installationid}/accesstokens",
            headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"},
        )

    access_token = resp.json()["token"]

    return httpx.AsyncClient(
        headers={"Authorization": f"token {access_token}", "Accept": "application/vnd.github+json"}
    )
