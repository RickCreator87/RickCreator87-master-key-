🏗️ Repo Setup — app/logic/repo_setup.py

`python
from app.ai.modelrouter import routeto_model
from app.server.githubclient import getinstallation_client
import base64

async def handlerepoevent(payload: dict):
    if payload["action"] != "created":
        return

    repo = payload["repository"]
    installation_id = payload["installation"]["id"]

    client = await getinstallationclient(installation_id)

    ai = await routetomodel("reposetup", text=f"Initialize {repo['fullname']}")

    readme = ai["choices"][0]["message"]["content"]

    await client.put(
        f"https://api.github.com/repos/{repo['owner']['login']}/{repo['name']}/contents/README.md",
        json={
            "message": "Initialize README via Master AI",
            "content": base64.b64encode(readme.encode()).decode(),
        },
    )
