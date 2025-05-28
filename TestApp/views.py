import os
import pandas as pd
import requests
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings
from decouple import config  # ✅ import decouple
from .models import MessageTemplate, Contact, MessageLog

# Home view
def index(request):
    return render(request, 'TestApp/index.html')

# Protected: Send Message
@login_required(login_url='/login/')
def send_message(request):
    if request.method == 'POST':
        template_name = request.POST['template_name']
        message_text = request.POST['message_text']
        media = request.FILES.get('media')
        excel_file = request.FILES['excel_file']

        template = MessageTemplate.objects.create(
            name=template_name,
            text=message_text,
            media=media
        )

        df = pd.read_excel(excel_file)
        for _, row in df.iterrows():
            name = row['Name']
            phone = row['Contact']
            contact = Contact.objects.create(name=name, phone_number=phone)
            status = send_whatsapp_message(phone, message_text, media)
            MessageLog.objects.create(contact=contact, template=template, status=status)

        messages.success(request, "Messages sent successfully.")
        return render(request, 'TestApp/message_sent.html', {'template': template})

    return render(request, 'TestApp/send_message.html')


# ✅ WhatsApp API - secure version with environment variables
def send_whatsapp_message(phone, message, media):
    url = config('WHATSAPP_API_URL')  # ✅ URL from .env
    headers = {
        'Authorization': f'Bearer {config("WHATSAPP_ACCESS_TOKEN")}',  # ✅ Token from .env
        'Content-Type': 'application/json'
    }
    data = {
        'messaging_product': 'whatsapp',
        'to': phone,
        'type': 'text',
        'text': {'body': message}
    }
    response = requests.post(url, headers=headers, json=data)
    return 'Sent' if response.status_code == 200 else 'Failed'


# Login View with message and redirect
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            next_url = request.POST.get('next') or request.GET.get('next') or '/'
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'TestApp/login.html')

    return render(request, 'TestApp/login.html')


# Signup view with message
@csrf_exempt
def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Signup successful! Please log in.")
            return redirect('login')
        else:
            messages.error(request, "Signup failed. Please correct the errors.")
    else:
        form = UserCreationForm()
    return render(request, 'TestApp/signup.html', {'form': form})


# Logout
def logout_view(request):
    logout(request)
    return redirect('login')


# AJAX: Check login
def check_login(request):
    return JsonResponse({'logged_in': request.user.is_authenticated})


# AJAX login
@csrf_exempt
def ajax_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})
