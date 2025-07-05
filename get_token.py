import os
import requests
from dotenv import load_dotenv

# Load .env file
load_dotenv()

client_id = os.getenv("EBAY_CLIENT_ID")
client_secret = os.getenv("EBAY_CLIENT_SECRET")
redirect_uri = os.getenv("EBAY_REDIRECT_URI")
auth_code = os.getenv("EBAY_AUTH_CODE")
environment = os.getenv("EBAY_ENVIRONMENT", "production")

# Select endpoint based on environment
token_url = (
    "https://api.ebay.com/identity/v1/oauth2/token"
    if environment == "production"
    else "https://api.sandbox.ebay.com/identity/v1/oauth2/token"
)

headers = {
    "Content-Type": "application/x-www-form-urlencoded",
}

auth = (client_id, client_secret)

data = {
    "grant_type": "authorization_code",
    "code": auth_code,
    "redirect_uri": redirect_uri,
}

response = requests.post(token_url, headers=headers, auth=auth, data=data)

print("Response:", response.status_code)
print("Token JSON:")
print(response.json())
