from django.db import models
from django.contrib.auth.models import User
from cryptography.fernet import Fernet
import base64
from django.conf import settings
import os

# Generate or load a key for encryption
KEY_FILE = os.path.join(settings.BASE_DIR, 'vault.key')
def get_encryption_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, 'wb') as f:
            f.write(key)
    else:
        with open(KEY_FILE, 'rb') as f:
            key = f.read()
    return key

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
