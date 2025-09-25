import hmac
import hashlib
import json
import requests
import tarfile
import io
import os
from fastapi import HTTPException

API_BASE = "https://api.github.com"


class GH:
    def __init__(self, token: str, webhook_secret: str):
        self.token = token
        self.webhook_secret = webhook_secret.encode()

    def verify_signature(self, body: bytes, signature: str | None):
        if not signature:
            raise HTTPException(status_code=400, detail="Missing signature")
        mac = hmac.new(self.webhook_secret, msg=body, digestmod=hashlib.sha256)
        expected = f"sha256={mac.hexdigest()}"
        if not hmac.compare_digest(expected, signature):
            raise HTTPException(status_code=401, detail="Bad signature")

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json"
        }

    def list_changed_files(self, repo_full: str, pr_number: int):
        url = f"{API_BASE}/repos/{repo_full}/pulls/{pr_number}/files"
        r = requests.get(url, headers=self._headers())
        r.raise_for_status()
        return [f["filename"] for f in r.json()]

    def post_pr_comment(self, repo_full: str, pr_number: int, markdown: str):
        url = f"{API_BASE}/repos/{repo_full}/issues/{pr_number}/comments"
        r = requests.post(url, headers=self._headers(), json={"body": markdown})
        r.raise_for_status()
        return r.json()

    def checkout_ref(self, repo_full: str, sha: str, dest: str):
        # Simple fetch via archive, avoids managing SSH keys on server.
        url = f"{API_BASE}/repos/{repo_full}/tarball/{sha}"
        r = requests.get(url, headers=self._headers(), stream=True)
        r.raise_for_status()
        
        tf = tarfile.open(fileobj=io.BytesIO(r.content), mode="r:*")
        tf.extractall(dest)
        # repo extracts into a single subdir; return its path
        subdir = [d for d in os.listdir(dest) if os.path.isdir(os.path.join(dest, d))][0]
        return os.path.join(dest, subdir)