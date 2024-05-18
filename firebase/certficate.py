from os import environ
import firebase_admin
from firebase_admin import credentials

class Certificate(credentials.Certificate):
    def __init__(self, credential = None):
        cred = {
            "type": environ.get("FIREBASE_TYPE"),
            "project_id": environ.get("FIREBASE_PROJECT_ID"),
            "private_key_id": environ.get("FIREBASE_PRIVATE_KEY_ID"),
            "private_key": environ.get("FIREBASE_PRIVATE_KEY").replace("\\n", "\n"),
            "client_email": environ.get("FIREBASE_CLIENT_EMAIL"),
            "client_id": environ.get("FIREBASE_CLIENT_ID"),
            "auth_uri": environ.get("FIREBASE_AUTH_URI"),
            "token_uri": environ.get("FIREBASE_TOKEN_URI"),
            "auth_provider_x509_cert_url": environ.get("FIREBASE_AUTH_PROVIDER_X509_CERT_URL"),
            "client_x509_cert_url": environ.get("FIREBASE_CLIENT_X509_CERT_URL"),
        }
        super().__init__(cred if credential == None else credential)