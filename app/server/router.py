🧭 Event Router

app/server/router.py

`python
from app.logic.pranalysis import handlepr
from app.logic.reposetup import handlerepoevent, handlepush
from app.logic.ciadvice import handleworkflow_run
from app.logic.onboarding import handle_installation

async def route_event(event: str | None, payload: dict):
    match event:
        case "pull_request":
            return await handle_pr(payload)
        case "push":
            return await handle_push(payload)
        case "workflow_run":
            return await handleworkflowrun(payload)
        case "repository":
            return await handlerepoevent(payload)
        case "installation":
            return await handle_installation(payload)
        case _:
            return
