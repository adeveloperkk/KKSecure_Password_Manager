from django.db import models
from django.contrib.auth.models import User
from cryptography.fernet import Fernet
import base64
from django.conf import settings
import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load encryption key from environment variable
VAULT_KEY = os.environ.get('VAULT_KEY')
if VAULT_KEY is None:
    raise ValueError('VAULT_KEY environment variable not set')
# If the key is base64 encoded, ensure it's bytes
def get_encryption_key():
    return VAULT_KEY.encode()

def encrypt_password(raw_password):
    key = get_encryption_key()
    f = Fernet(key)
    return f.encrypt(raw_password.encode()).decode()

def decrypt_password(token):
    key = get_encryption_key()
    f = Fernet(key)
    return f.decrypt(token.encode()).decode()

# Create your models here.

class PasswordEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    site_name = models.CharField(max_length=255)
    site_url = models.URLField(blank=True)
    username = models.CharField(max_length=255)
    password_encrypted = models.TextField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.site_name} ({self.username})"
