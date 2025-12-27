🧠 Logic Modules

PR Analysis — app/logic/pr_analysis.py

`python
from app.ai.modelrouter import routeto_model
from app.server.githubclient import getinstallation_client

async def handle_pr(payload: dict):
    if payload["action"] not in ["opened", "synchronize", "reopened"]:
        return

    installation_id = payload["installation"]["id"]
    repo = payload["repository"]
    pr = payload["pull_request"]

    client = await getinstallationclient(installation_id)

    files = await client.get(
        f"https://api.github.com/repos/{repo['owner']['login']}/{repo['name']}/pulls/{pr['number']}/files"
    )

    code_context = "\n\n".join(
        f"{f['filename']}\n{f.get('patch', '')}" for f in files.json()
    )

    ai = await routetomodel("pranalysis", text=pr["title"], code=codecontext)

    await client.post(
        f"https://api.github.com/repos/{repo['owner']['login']}/{repo['name']}/issues/{pr['number']}/comments",
        json={"body": ai["choices"][0]["message"]["content"]},
    )
