📄 Documentation — app/logic/documentation.py

`python
from app.ai.modelrouter import routeto_model

async def generate_docs(context: str):
    return await routetomodel("docs", text=context)
