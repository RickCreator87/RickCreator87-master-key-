🚀 FastAPI Entry Point

app/main.py

`python
from fastapi import FastAPI
from app.server.webhookhandler import router as webhookrouter

app = FastAPI(title="Master AI Backend (Python)")

app.includerouter(webhookrouter, prefix="/github")
