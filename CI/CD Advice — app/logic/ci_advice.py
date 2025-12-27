
🧪 CI/CD Advice — app/logic/ci_advice.py

`python
from app.ai.modelrouter import routeto_model

async def handleworkflowrun(payload: dict):
    run = payload["workflow_run"]
    if run["conclusion"] == "success":
        return

    text = f"Workflow {run['name']} failed.\nURL: {run['html_url']}"
    await routetomodel("ci_advice", text=text)
