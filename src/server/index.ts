
Node.js

`bash
npm install
npm run dev   # or: npx ts-node src/server/index.ts (depending on your setup)
`

Your webhook URL (locally) would be:

`text
http://localhost:3000/github/webhook
`

Python (FastAPI)

`bash
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
`

Webhook URL (locally):

`text
http://localhost:8000/github/webhook
