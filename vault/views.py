from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import PasswordEntry, encrypt_password, decrypt_password, WalletEntry, Note, SaveEvent
from .forms import WalletEntryForm, NoteForm
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import csv
from io import TextIOWrapper
import random
import string
from django.db.models import Q

@login_required
def password_list(request):
    query = request.GET.get('q', '')
    filter_by = request.GET.get('filter_by', '')
    passwords = PasswordEntry.objects.filter(user=request.user)
    if query:
        passwords = passwords.filter(
            Q(site_name__icontains=query) |
            Q(username__icontains=query) |
            Q(site_url__icontains=query) |
            Q(notes__icontains=query)
        )
    if filter_by == 'recent':
        passwords = passwords.order_by('-created_at')
    elif filter_by == 'site':
        passwords = passwords.order_by('site_name')
    elif filter_by == 'username':
        passwords = passwords.order_by('username')
    elif filter_by == 'url':
        passwords = passwords.order_by('site_url')
    elif filter_by == 'note':
        passwords = passwords.order_by('notes')
    return render(request, 'vault/password_list.html', {
        'passwords': passwords,
        'query': query,
        'filter_by': filter_by
    })

@login_required
def password_detail(request, pk):
    entry = get_object_or_404(PasswordEntry, pk=pk, user=request.user)
    entry.password_encrypted = decrypt_password(entry.password_encrypted)
    return render(request, 'vault/password_detail.html', {'entry': entry})

@login_required
def password_create(request):
    if request.method == 'POST':
        site_name = request.POST['site_name']
        site_url = request.POST['site_url']
        username = request.POST['username']
        password_encrypted = encrypt_password(request.POST['password'])
        notes = request.POST.get('notes', '')
        PasswordEntry.objects.create(
            user=request.user,
            site_name=site_name,
            site_url=site_url,
            username=username,
            password_encrypted=password_encrypted,
            notes=notes
        )
        return redirect('password_list')
    return render(request, 'vault/password_form.html')

@login_required
def password_edit(request, pk):
    entry = get_object_or_404(PasswordEntry, pk=pk, user=request.user)
    if request.method == 'POST':
        entry.site_name = request.POST['site_name']
        entry.site_url = request.POST['site_url']
        entry.username = request.POST['username']
        entry.password_encrypted = encrypt_password(request.POST['password'])
        entry.notes = request.POST.get('notes', '')
        entry.save()
        return redirect('password_list')
    # Decrypt password for display in form
    entry.password_encrypted = decrypt_password(entry.password_encrypted)
    return render(request, 'vault/password_form.html', {'entry': entry})

@login_required
def password_delete(request, pk):
    entry = get_object_or_404(PasswordEntry, pk=pk, user=request.user)
    if request.method == 'POST':
        entry.delete()
        return redirect('password_list')
    return render(request, 'vault/password_confirm_delete.html', {'entry': entry})

@login_required
def generate_password(request):
    length = int(request.GET.get('length', 16))
    chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(chars) for _ in range(length))
    return JsonResponse({'password': password})

@login_required
def wallet_list(request):
    wallets = WalletEntry.objects.filter(user=request.user)
    return render(request, 'vault/wallet_list.html', {'wallets': wallets})

@login_required
def wallet_detail(request, pk):
    wallet = get_object_or_404(WalletEntry, pk=pk, user=request.user)
    return render(request, 'vault/wallet_detail.html', {'wallet': wallet})

@login_required
def wallet_create(request):
    # Pre-fill form fields from GET params
    initial = {}
    wallet_type = request.GET.get('wallet_type') or request.GET.get('type')
    card_type = request.GET.get('card_type')
    if wallet_type:
        initial['wallet_type'] = wallet_type
        if wallet_type == 'card' and card_type:
            initial['card_type'] = card_type
        elif wallet_type == 'card' and request.GET.get('type') in ['credit', 'debit']:
            initial['card_type'] = request.GET.get('type')
    if request.method == 'POST':
        form = WalletEntryForm(request.POST)
        if form.is_valid():
            wallet = form.save(commit=False)
            wallet.user = request.user
            wallet.save()
            return redirect('wallet_list')
    else:
        form = WalletEntryForm(initial=initial)
    return render(request, 'vault/wallet_form.html', {'form': form})

@login_required
def wallet_edit(request, pk):
    wallet = get_object_or_404(WalletEntry, pk=pk, user=request.user)
    if request.method == 'POST':
        form = WalletEntryForm(request.POST, instance=wallet)
        if form.is_valid():
            form.save()
            return redirect('wallet_detail', pk=wallet.pk)
    else:
        form = WalletEntryForm(instance=wallet)
    return render(request, 'vault/wallet_form.html', {'form': form})

@login_required
def wallet_delete(request, pk):
    wallet = get_object_or_404(WalletEntry, pk=pk, user=request.user)
    if request.method == 'POST':
        wallet.delete()
        return redirect('wallet_list')
    return render(request, 'vault/wallet_confirm_delete.html', {'wallet': wallet})

@login_required
def note_list(request):
    query = request.GET.get('q', '')
    notes = Note.objects.filter(user=request.user)
    if query:
        notes = notes.filter(title__icontains=query)
    notes = notes.order_by('title')
    return render(request, 'vault/note_list.html', {
        'notes': notes,
        'query': query,
        'note_count': notes.count(),
    })

@login_required
def note_create(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            return redirect('note_list')
    else:
        form = NoteForm()
    return render(request, 'vault/note_form.html', {'form': form})

@login_required
def note_edit(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('note_list')
    else:
        form = NoteForm(instance=note)
    return render(request, 'vault/note_form.html', {'form': form, 'edit': True})

@login_required
def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == 'POST':
        note.delete()
        return redirect('note_list')
    return render(request, 'vault/note_confirm_delete.html', {'note': note})

@login_required
def note_detail(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    return render(request, 'vault/note_detail.html', {'note': note})

@login_required
def save_event_list(request):
    events = SaveEvent.objects.filter(user=request.user).order_by('-event_date')
    return render(request, 'vault/save_event_list.html', {'events': events})

@login_required
def save_event_detail(request, pk):
    event = get_object_or_404(SaveEvent, pk=pk, user=request.user)
    return render(request, 'vault/save_event_detail.html', {'event': event})

@login_required
def save_event_create(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST.get('description', '')
        event_date = request.POST['event_date']
        SaveEvent.objects.create(
            user=request.user,
            title=title,
            description=description,
            event_date=event_date
        )
        return redirect('save_event_list')
    return render(request, 'vault/save_event_form.html')

@login_required
def save_event_edit(request, pk):
    event = get_object_or_404(SaveEvent, pk=pk, user=request.user)
    if request.method == 'POST':
        event.title = request.POST['title']
        event.description = request.POST.get('description', '')
        event.event_date = request.POST['event_date']
        event.save()
        return redirect('save_event_list')
    return render(request, 'vault/save_event_form.html', {'event': event, 'edit': True})

@login_required
def save_event_delete(request, pk):
    event = get_object_or_404(SaveEvent, pk=pk, user=request.user)
    if request.method == 'POST':
        event.delete()
        return redirect('save_event_list')
    return render(request, 'vault/save_event_confirm_delete.html', {'event': event})

@login_required
def password_generator(request):
    return render(request, 'vault/password_generator.html')

@login_required
def export_all_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="exported_credentials.csv"'

    writer = csv.writer(response)
    writer.writerow(['name', 'url', 'username', 'password', 'note'])

    # Export Password Entries
    passwords = PasswordEntry.objects.filter(user=request.user)
    for password in passwords:
        writer.writerow([password.site_name, password.site_url, password.username, decrypt_password(password.password_encrypted), password.notes])

    return response

@csrf_exempt
@login_required
def import_all_data(request):
    if request.method == 'POST':
        try:
            if 'csvfile' not in request.FILES:
                return JsonResponse({'status': 'error', 'message': 'No file uploaded'}, status=400)

            file = request.FILES['csvfile']
            if not file.name.endswith('.csv'):
                return JsonResponse({'status': 'error', 'message': 'Uploaded file is not a CSV file'}, status=400)

            data = TextIOWrapper(file.file, encoding='utf-8')
            reader = csv.DictReader(data)

            required_columns = {'name', 'url', 'username', 'password'}
            if not required_columns.issubset(reader.fieldnames):
                return JsonResponse({'status': 'error', 'message': 'Invalid CSV format. Missing required columns: ' + ', '.join(required_columns - set(reader.fieldnames))}, status=400)

            for row in reader:
                PasswordEntry.objects.create(
                    user=request.user,
                    site_name=row['name'],
                    site_url=row['url'],
                    username=row['username'],
                    password_encrypted=encrypt_password(row['password'])
                )

            return redirect('import_success')
        except csv.Error as e:
            return render(request, 'vault/import_all.html', {'error_message': 'CSV parsing error: ' + str(e)})
        except Exception as e:
            return render(request, 'vault/import_all.html', {'error_message': 'Unexpected error: ' + str(e)})
    return render(request, 'vault/import_all.html')

@login_required
def import_success(request):
    return render(request, 'vault/import_success.html')
