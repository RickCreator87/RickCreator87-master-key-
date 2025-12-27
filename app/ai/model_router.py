
🤖 AI Model Router

app/ai/model_router.py

`python
from app.ai.deepseek import call_deepseek
from app.ai.ollama import call_ollama
from app.ai.openaiclient import callopenai

async def routetomodel(task: str, text: str = "", code: str = "", preferred: str | None = None):
    target = preferred or pick_default(task)

    if target == "deepseek":
        return await call_deepseek(task, text, code)
    if target == "ollama":
        return await call_ollama(task, text, code)
    if target == "openai":
        return await call_openai(task, text, code)

def pick_default(task: str):
    if task in ["pranalysis", "ciadvice"]:
        return "deepseek"
    if task in ["docs", "onboarding"]:
        return "openai"
    return "ollama"
