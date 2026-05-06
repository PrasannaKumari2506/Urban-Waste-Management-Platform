from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
from datetime import datetime, timedelta, timezone
import requests
import uuid
from .models import User, UserSession

def login_view(request):
    if request.user.is_authenticated:
        return redirect('households:dashboard' if request.user.role == 'household' else 'recyclers:dashboard')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                login(request, user)
                messages.success(request, f'Welcome back, {user.name}!')
                
                # Redirect based on role
                if user.role == 'household':
                    return redirect('households:dashboard')
                elif user.role == 'recycler':
                    return redirect('recyclers:dashboard')
                else:
                    return redirect('home')
            else:
                messages.error(request, 'Invalid email or password')
        except User.DoesNotExist:
            messages.error(request, 'Invalid email or password')
    
    return render(request, 'accounts/login.html')

def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        name = request.POST.get('name')
        role = request.POST.get('role', 'household')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'accounts/register.html')
        
        user = User.objects.create_user(
            email=email,
            password=password,
            name=name,
            role=role
        )
        
        if role == 'recycler':
            from recyclers.models import RecyclerProfile
            RecyclerProfile.objects.create(user=user)
        
        login(request, user)
        messages.success(request, 'Registration successful!')
        return redirect('households:dashboard' if role == 'household' else 'recyclers:dashboard')
    
    return render(request, 'accounts/register.html')

def logout_view(request):
    if request.user.is_authenticated:
        UserSession.objects.filter(user=request.user).delete()
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('home')

@csrf_exempt
def auth_callback(request):
    """Handle Emergent Auth OAuth callback"""
    session_id = request.GET.get('session_id')
    if not session_id:
        messages.error(request, 'Invalid authentication session')
        return redirect('accounts:login')
    
    try:
        response = requests.get(
            settings.EMERGENT_SESSION_DATA_URL,
            headers={'X-Session-ID': session_id},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        
        email = data.get('email')
        name = data.get('name')
        picture = data.get('picture')
        session_token = data.get('session_token')
        
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'name': name,
                'profile_picture': picture,
                'role': request.session.get('pending_role', 'household')
            }
        )
        
        if not created:
            user.name = name
            user.profile_picture = picture
            user.save()
        
        if created and user.role == 'recycler':
            from recyclers.models import RecyclerProfile
            RecyclerProfile.objects.create(user=user)
        
        expires_at = datetime.now(timezone.utc) + timedelta(days=7)
        UserSession.objects.create(
            user=user,
            session_token=session_token,
            expires_at=expires_at
        )
        
        login(request, user)
        
        if 'pending_role' in request.session:
            del request.session['pending_role']
        
        messages.success(request, f'Welcome, {user.name}!')
        return redirect('households:dashboard' if user.role == 'household' else 'recyclers:dashboard')
        
    except Exception as e:
        messages.error(request, f'Authentication failed: {str(e)}')
        return redirect('accounts:login')

@csrf_exempt
def session_view(request):
    """Store pending role for OAuth flow"""
    if request.method == 'POST':
        role = request.POST.get('role', 'household')
        request.session['pending_role'] = role
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})
