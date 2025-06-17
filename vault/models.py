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

class WalletEntry(models.Model):
    ACCOUNT = 'account'
    CREDIT = 'credit'
    DEBIT = 'debit'
    WALLET_TYPE_CHOICES = [
        (ACCOUNT, 'Account Number'),
        (CREDIT, 'Credit Card'),
        (DEBIT, 'Debit Card'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wallet_type = models.CharField(max_length=10, choices=WALLET_TYPE_CHOICES)
    # Card fields
    card_number = models.CharField(max_length=20, blank=True)
    card_holder = models.CharField(max_length=255, blank=True)
    card_expiry = models.CharField(max_length=7, blank=True)  # MM/YYYY
    card_cvv = models.CharField(max_length=4, blank=True)
    # Bank account fields
    bank_name = models.CharField(max_length=255, blank=True)
    account_number = models.CharField(max_length=30, blank=True)
    ifsc_code = models.CharField(max_length=20, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.wallet_type == self.CREDIT:
            return f"Credit Card: {self.card_number} ({self.card_holder})"
        elif self.wallet_type == self.DEBIT:
            return f"Debit Card: {self.card_number} ({self.card_holder})"
        else:
            return f"Account: {self.bank_name} ({self.account_number})"

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class SaveEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    event_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.event_date})"


class SystemLog(models.Model):
    ACTION_CHOICES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('terminate', 'Terminate Session'),
        ('terminate_all', 'Terminate All Sessions'),
        ('delete', 'Delete Session'),
        ('create', 'Create Object'),
        ('update', 'Update Object'),
        ('delete_obj', 'Delete Object'),
        # Add more as needed
    ]
    admin_user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=32, choices=ACTION_CHOICES)
    object_type = models.CharField(max_length=64, blank=True, null=True)
    object_id = models.CharField(max_length=64, blank=True, null=True)
    session_key = models.CharField(max_length=40, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True)

    def __str__(self):
        return f"{self.admin_user} {self.action} {self.object_type} {self.object_id} at {self.timestamp}"
