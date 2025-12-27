```yaml
version: "3.9"

services:
  master-ai-backend:
    build: .
    container_name: master-ai-backend-python
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - ollama

  ollama:
    image: ollama/ollama:latest
    container_name: ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama-data:/root/.ollama

volumes:
  ollama-data:
```

Then:

```bash
docker compose up --build
```

Your webhook URL (once deployed) will be:

```text
https://<your-deployed-domain>/github/webhook
```

Locally with docker-compose:

```text
http://localhost:8000/github/webhook
```
