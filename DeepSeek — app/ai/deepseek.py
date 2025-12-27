🧩 AI Clients

DeepSeek — app/ai/deepseek.py

`python
import httpx
from app.utils.config import config

async def call_deepseek(task: str, text: str, code: str):
    prompt = f"Task: {task}\n\nText:\n{text}\n\nCode:\n{code}"
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {config.DEEPSEEKAPIKEY}"},
            json={"model": "deepseek-chat", "messages": [{"role": "user", "content": prompt}]},
        )
    return resp.json()
`

Ollama — app/ai/ollama.py

`python
import httpx
from app.utils.config import config

async def call_ollama(task: str, text: str, code: str):
    prompt = f"{task}\n\n{text}\n\n{code}"
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{config.OLLAMA_HOST}/api/generate",
            json={"model": "llama3", "prompt": prompt},
        )
    return resp.json()
`

OpenAI — app/ai/openai_client.py

`python
import httpx
from app.utils.config import config

async def call_openai(task: str, text: str, code: str):
    prompt = f"Task: {task}\n\n{text}\n\n{code}"
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {config.OPENAIAPIKEY}"},
            json={"model": "gpt-4o-mini", "messages": [{"role": "user", "content": prompt}]},
        )
    return resp.json()
