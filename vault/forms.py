from django import forms
from .models import WalletEntry, Note

class WalletEntryForm(forms.ModelForm):
    class Meta:
        model = WalletEntry
        fields = [
            'wallet_type',
            'card_number', 'card_holder', 'card_expiry', 'card_cvv',
            'bank_name', 'account_number', 'ifsc_code',
            'notes'
        ]

    def clean(self):
        cleaned_data = super().clean()
        wallet_type = cleaned_data.get('wallet_type')
        # Always require card fields for credit/debit, and account fields for account
        if wallet_type == WalletEntry.CREDIT or wallet_type == WalletEntry.DEBIT:
            missing = []
            if not cleaned_data.get('card_number'):
                missing.append('Card number')
            if not cleaned_data.get('card_holder'):
                missing.append('Card holder')
            if not cleaned_data.get('card_expiry'):
                missing.append('Card expiry')
            if not cleaned_data.get('card_cvv'):
                missing.append('Card CVV')
            # Use card_bank_name from POST if present
            card_bank_name = self.data.get('card_bank_name')
            if not card_bank_name:
                missing.append('Bank name')
            else:
                cleaned_data['bank_name'] = card_bank_name
            if missing:
                raise forms.ValidationError('Required: ' + ', '.join(missing))
        elif wallet_type == WalletEntry.ACCOUNT:
            missing = []
            if not cleaned_data.get('bank_name'):
                missing.append('Bank name')
            if not cleaned_data.get('account_number'):
                missing.append('Account number')
            # Use account_holder from POST if present
            account_holder = self.data.get('account_holder')
            if not account_holder:
                missing.append('A/C Holder')
            else:
                cleaned_data['card_holder'] = account_holder
            if not cleaned_data.get('ifsc_code'):
                missing.append('IFSC code')
            if missing:
                raise forms.ValidationError('Required: ' + ', '.join(missing))
        return cleaned_data

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content']
