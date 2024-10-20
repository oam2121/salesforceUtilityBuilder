import requests
import os

def authenticate_salesforce():
    SF_USERNAME = os.getenv('SF_USERNAME', 'oam@ciklum.com')
    SF_PASSWORD = os.getenv('SF_PASSWORD', 'Mayuri@123')
    SF_SECURITY_TOKEN = os.getenv('SF_SECURITY_TOKEN', 'UEmSON8Bgh3nqd7u52qtJoPk')
    SF_CLIENT_ID = os.getenv('SF_CLIENT_ID', '3MVG9WVXk15qiz1JeBLjx2dvU8zQH3eEbErpxXBi69g_7ZPDHX9kyM5rfO2erHB38vJWXlRee2nUpMUAFAJ9_')
    SF_CLIENT_SECRET = os.getenv('SF_CLIENT_SECRET', '5ECD6E692B08BC05856E4997BE0497D8F817F9F12B36EFA0A8D5D022551F4571')
    
    token_url = "https://login.salesforce.com/services/oauth2/token"
    
    payload = {
        'grant_type': 'password',
        'client_id': SF_CLIENT_ID,
        'client_secret': SF_CLIENT_SECRET,
        'username': SF_USERNAME,
        'password': SF_PASSWORD + SF_SECURITY_TOKEN
    }

    print("Sending payload for Salesforce authentication:", payload)  # Add this for debugging
    
    response = requests.post(token_url, data=payload)
    
    print("Salesforce authentication response status:", response.status_code)  # Add this for debugging
    print("Salesforce authentication response text:", response.text)  # Add this for debugging
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to authenticate with Salesforce: {response.text}")

