import re
import requests
import json
import sys
import os

def generate_email_body():
    filename = 'changelog.txt'

    # Used for development and testing
    if not os.path.exists(filename):
        filename = 'sample.txt'

    with open("changelog.txt", 'r') as file:
        count = sum(1 for _ in file)

        if count <= 2:
            filename = 'sample.txt'

    output = ""
    change_differential = ""
    changes_url = ""

    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('##'):
                output += "<h2>" + line.strip().removeprefix("##") + "</h2><ul>"
            elif line.startswith('* '):
                newline = line.strip().removeprefix("* ")

                url = newline.split(" ")[-1]
                pr_id = newline.split("/")[-1]

                newline = newline.removesuffix(url)
                newline += f"<a href=\"{url}\">#{pr_id}</a>"

                output += "<li>" + newline + "</li>"
            elif line.startswith("**Full Changelog**"):
                changes_url = line.split(" ")[-1]
                change_differential = line.split("/")[-1]

                output += f"<h2>Full Changelog</h2><a href=\"{changes_url}\">{change_differential}</a>"
            else:
                output += "</ul>" + line.strip()

    template_filename = "template.html"

    with open(template_filename, 'r') as file:
        content = file.read()

    pattern = r"https://github\.com/[A-Za-z0-9_-]+/([A-Za-z0-9_-]+)/"

    match = re.search(pattern, changes_url)
    if match:
        repo_name = match.group(1)

    version_number = change_differential.split("...")[-1]
    release_url = f"https://github.com/DevOps-2023-TeamA/{repo_name}/releases/tag/{version_number}"

    return (repo_name, content.replace("CHANGELOG_CONTENT", output).replace("VERSION_NUMBER", version_number).replace("REPO_NAME", repo_name).replace("RELEASE_URL", release_url))

def generate_sendgrid_body(to_emails, html_content, subject, sender_email):
    """
    Generate the JSON body for sending an email with SendGrid.

    Parameters:
    - to_emails: A list of recipient email addresses.
    - html_content: A string containing the HTML content of the email.
    - subject: The subject of the email.
    - sender_email: The sender's email address.

    Returns:
    - A dictionary representing the JSON payload for the SendGrid API.
    """
    if not isinstance(to_emails, list) or not to_emails:
        raise ValueError("to_emails must be a list of email addresses and cannot be empty.")

    to_field = [{"email": email} for email in to_emails]

    data = {
        "personalizations": [
            {
                "to": to_field,
                "subject": subject
            }
        ],
        "from": {
            "email": sender_email
        },
        "content": [
            {
                "type": "text/html",
                "value": html_content
            }
        ]
    }

    return data

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: script.py API_KEY email1@domain.com [email2@domain.com] ...")
        exit(1)
    
    SENDGRID_API_KEY = sys.argv[1]
    emails = sys.argv[2:]  # Capture all emails passed as arguments

    (repo_name, email_body) = generate_email_body()
    subject = f"A new release for {repo_name} is now available."
    sender_email = "tsao-pipeline@jiachen.app"

    email_data = generate_sendgrid_body(emails, email_body, subject, sender_email)

    response = requests.post(
        "https://api.sendgrid.com/v3/mail/send",
        headers={
            "Authorization": f"Bearer {SENDGRID_API_KEY}",
            "Content-Type": "application/json"
        },
        data=json.dumps(email_data)
    )

    print(response.status_code)
    if response.status_code >= 300 or response.status_code < 200:
        exit(1)
