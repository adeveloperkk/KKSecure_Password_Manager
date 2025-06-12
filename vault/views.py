from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import PasswordEntry, encrypt_password, decrypt_password
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
def import_passwords(request):
    if request.method == 'POST' and request.FILES.get('csvfile'):
        csvfile = TextIOWrapper(request.FILES['csvfile'].file, encoding='utf-8')
        reader = csv.DictReader(csvfile)
        for row in reader:
            PasswordEntry.objects.create(
                user=request.user,
                site_name=row.get('site_name', ''),
                site_url=row.get('site_url', ''),
                username=row.get('username', ''),
                password_encrypted=encrypt_password(row.get('password', '')),
                notes=row.get('notes', '')
            )
        return redirect('password_list')
    return render(request, 'vault/import_passwords.html')

@login_required
def export_passwords(request):
    passwords = PasswordEntry.objects.filter(user=request.user)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="passwords_export.csv"'
    writer = csv.writer(response)
    writer.writerow(['site_name', 'site_url', 'username', 'password', 'notes'])
    for entry in passwords:
        writer.writerow([
            entry.site_name,
            entry.site_url,
            entry.username,
            decrypt_password(entry.password_encrypted),
            entry.notes
        ])
    return response
