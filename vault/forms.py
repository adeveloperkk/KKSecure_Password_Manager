from django import forms
from .models import WalletEntry, Note

class WalletEntryForm(forms.ModelForm):
    class Meta:
        model = WalletEntry
        fields = [
            'wallet_type',
            'card_type',  # new field
            'card_number', 'card_holder', 'card_expiry', 'card_cvv',
            'bank_name', 'account_number', 'ifsc_code',
            'notes'
        ]

    def clean(self):
        cleaned_data = super().clean()
        wallet_type = cleaned_data.get('wallet_type')
        if wallet_type == WalletEntry.CARD:
            if not cleaned_data.get('card_number') or not cleaned_data.get('card_holder') or not cleaned_data.get('bank_name'):
                raise forms.ValidationError('Card details and bank name are required.')
        elif wallet_type == WalletEntry.BANK:
            if not cleaned_data.get('bank_name') or not cleaned_data.get('account_number'):
                raise forms.ValidationError('Bank account details are required.')
        return cleaned_data

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content']
