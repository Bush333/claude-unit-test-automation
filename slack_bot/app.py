
import os
import re
import requests

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

app = App(token=os.environ["SLACK_BOT_TOKEN"])

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]

REPO = "Bush333/claude-unit-test-automation"
WORKFLOW = "generate-unit-tests.yml"


@app.event("app_mention")
def handle_mention(event, say):
    text = event.get("text", "")

    pattern = (
        r"https://github\.com/"
        r"Bush333/claude-unit-test-automation/"
        r"pull/(\d+)"
    )

    match = re.search(pattern, text)

    if not match:
        say(
            "Please provide a valid PR URL from "
            "Bush333/claude-unit-test-automation."
        )
        return

    pr_number = match.group(1)

    url = (
        f"https://api.github.com/repos/{REPO}/"
        f"actions/workflows/{WORKFLOW}/dispatches"
    )

    response = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
        json={
            "ref": "main",
            "inputs": {
                "pr_number": pr_number
            }
        },
        timeout=20,
    )

    if response.status_code == 204:
        say(
            f"🚀 Unit-test generation started for PR #{pr_number}.\n"
            f"https://github.com/{REPO}/pull/{pr_number}"
        )
    else:
        say(
            f"❌ Unable to start workflow for PR #{pr_number}. "
            f"GitHub returned HTTP {response.status_code}."
        )


if __name__ == "__main__":
    SocketModeHandler(
        app,
        os.environ["SLACK_APP_TOKEN"]
    ).start()
