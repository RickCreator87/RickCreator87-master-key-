🧰 Utils

app/utils/config.py

`python
import os
import base64

class Config:
    PORT = int(os.getenv("PORT", 8000))

    GITHUBAPPID = os.getenv("GITHUBAPPID")
    GITHUBWEBHOOKSECRET = os.getenv("GITHUBWEBHOOKSECRET")

    GITHUBPRIVATEKEYBASE64 = os.getenv("GITHUBPRIVATEKEYBASE64")
    GITHUBPRIVATEKEY = base64.b64decode(GITHUBPRIVATEKEYBASE64).decode() if GITHUBPRIVATEKEYBASE64 else None

    DEEPSEEKAPIKEY = os.getenv("DEEPSEEKAPIKEY")
    OPENAIAPIKEY = os.getenv("OPENAIAPIKEY")
    OLLAMAHOST = os.getenv("OLLAMAHOST", "http://localhost:11434")

config = Config()
`

app/utils/logger.py

`python
def logger(level: str, message: str, meta: dict | None = None):
    print(f"[{level}] {message}", meta or "")

logger.info = lambda msg, meta=None: logger("INFO", msg, meta)
logger.warn = lambda msg, meta=None: logger("WARN", msg, meta)
logger.error = lambda msg, meta=None: logger("ERROR", msg, meta)
