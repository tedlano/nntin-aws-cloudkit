import os
import base64
import requests
import random
from datetime import datetime

from aws_lambda_powertools import Logger

SERVICE_NAME = os.getenv("POWERTOOLS_SERVICE_NAME")
LOG_LEVEL = os.getenv("LOG_LEVEL") or "INFO"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_REPO = os.getenv("GITHUB_REPO")
FILE_PATH = "commit-log.txt"  # File being updated in the repo

logger = Logger(service=SERVICE_NAME, level=LOG_LEVEL)

def get_existing_content():
    """Fetches the current content and SHA of the file from GitHub."""
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{GITHUB_REPO}/contents/{FILE_PATH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        content = response.json()
        existing_text = base64.b64decode(content["content"]).decode("utf-8").strip()
        sha = content["sha"]
        return existing_text, sha
    elif response.status_code == 404:
        return "", None  # File doesn't exist yet
    else:
        raise Exception(f"GitHub API error: {response.status_code} - {response.text}")

def commit_to_github():
    """Appends a new log entry to commit-log.txt in the GitHub repo with an 85% chance."""

    # 85% Probability of Making a Commit
    rand_num = random.random()
    if rand_num > 0.85:
        logger.info(f"Skipping commit today (random chance applied {rand_num}).")
        return {"statusCode": 200, "body": "Skipped commit today."}
    
    commit_message = f"Daily commit on {datetime.now().isoformat()}"
    new_entry = f"Commit at {datetime. now().isoformat()}"

    try:
        existing_text, sha = get_existing_content()

        # Append new content
        updated_content = f"{existing_text}\n{new_entry}".strip()
        encoded_content = base64.b64encode(updated_content.encode()).decode("utf-8")

        # Prepare commit payload
        url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{GITHUB_REPO}/contents/{FILE_PATH}"
        headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
        payload = {
            "message": commit_message,
            "content": encoded_content,
            "branch": "main",
        }
        if sha:
            payload["sha"] = sha  # Include SHA if the file exists

        # Push commit
        response = requests.put(url, headers=headers, json=payload)
        if response.status_code in [200, 201]:
            print(f"✅ Commit successful: {response.json()['commit']['html_url']}")
        else:
            print(f"❌ Commit failed: {response.text}")

    except Exception as e:
        print(f"⚠️ Error committing to GitHub: {str(e)}")

def handler(event, context):
    commit_to_github()
    return {"statusCode": 200, "body": "Commit pushed successfully"}