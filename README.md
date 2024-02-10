# TSAO Pipeline Emails

> [!Important]
> This project uses Twillio Sendgrid's free tier (no credit card required).
> 
> It is limited to 100 emails per day
>
> For more information, and potentially more updated information, check [Twillio Sendgrid's Pricing](https://sendgrid.com/en-us/pricing)

## setup
> [!Warning]
> This repository is hard-coded with information specific to this use case.
>
> To use this for any other project, you will need to manually edit out specific references within the `main.py` and `template.html` files, notably,
> - In `main.py`, the `sender_email` is set to `tsao-pipeline@jiachen.app`
> - In `template.html`, the team's name is in the email body and is set as `DevOps-2023-TeamA`
1. Retrieve an API key from [Sendgrid](https://docs.sendgrid.com/api-reference/api-keys/create-api-keys)
2. Install Requests
```bash
pip install requests
```
3. To run it, use the following
> [!Note]
> You can add as many recipients as you want by chaining the email addresses as it uses a variadic parameter for emails.
```
Usage: main.py API_KEY email1@domain.com [email2@domain.com] ...
```
Example
```bash
python main.py MY_SENDGRID_API_KEY email1@domain.com email2@domain.com email3@domain.com email4@domain.com
```

## setting up for local development and testing
1. Create a file named "changelog.txt" to house an auto-generated changelog from GitHub.
> [!Note]
> Without the `changelog.txt` file, the program will fallback onto `sample.txt`. `sample.txt` is based on the Release Notes from
> [tsao-backend-svc 1.0.0-alpha.1](https://github.com/DevOps-2023-TeamA/tsao-backend-svc/releases/tag/1.0.0-alpha.1).

2. Run the command to execute the code.
3. Consider placing a placeholder value as the Sendgrid Token like "test" so it does not count against the API free tier usage limits.

## maintainers
- [Yee Jia Chen](https://github.com/jiachenyee) S10219344C
- [Isabelle Pak Yi Shan](https://github.com/isabellepakyishan) S10222456J
- [Ho Kuan Zher](https://github.com/Kuan-Zher) S10223870D
- [Cheah Seng Jun](https://github.com/DanielCheahSJ) S10227333K
- [Chua Guo Jun](https://github.com/GuojunLoser) S10227743H
