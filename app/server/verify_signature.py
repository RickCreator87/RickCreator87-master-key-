🔐 Webhook Signature Verification

app/server/verify_signature.py

`python
import hmac
import hashlib
from app.utils.config import config

def verifysignature(payload: bytes, signatureheader: str | None) -> bool:
    if not signature_header:
        return False

    secret = config.GITHUBWEBHOOKSECRET.encode()
    digest = "sha256=" + hmac.new(secret, payload, hashlib.sha256).hexdigest()

    return hmac.comparedigest(digest, signatureheader)
