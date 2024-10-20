# Optional: This can store constants or credentials securely
# config.py (backend config file)
import os
# Example:
TOKEN_URL = 'https://login.salesforce.com/services/oauth2/token'

# For future use, you could store environment variables or sensitive credentials here
class Config:
    SF_USERNAME = os.getenv('SF_USERNAME', 'oam@ciklum.com')
    SF_PASSWORD = os.getenv('SF_PASSWORD', 'Mayuri@123')
    SF_SECURITY_TOKEN = os.getenv('SF_SECURITY_TOKEN', 'UEmSON8Bgh3nqd7u52qtJoPk')
    SF_CLIENT_ID = os.getenv('SF_CLIENT_ID', '3MVG9WVXk15qiz1JeBLjx2dvU8zQH3eEbErpxXBi69g_7ZPDHX9kyM5rfO2erHB38vJWXlRee2nUpMUAFAJ9_')
    SF_CLIENT_SECRET = os.getenv('SF_CLIENT_SECRET', '5ECD6E692B08BC05856E4997BE0497D8F817F9F12B36EFA0A8D5D022551F4571')