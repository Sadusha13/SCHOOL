from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.utils.crypto import get_random_string

from home_auth.models import PasswordResetRequest

# Get the custom user model
User = get_user_model()

# Create your views here.

def signup_view(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        
        # Check if user with this email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'A user with this email already exists.')
            return render(request, 'authentication/register.html')
        
        # Check if username (which is email) already exists
        if User.objects.filter(username=email).exists():
            messages.error(request, 'A user with this email already exists.')
            return render(request, 'authentication/register.html')

        try:
            # Create user
            user = User.objects.create_user(
                username=email, 
                email=email, 
                password=password,
                first_name=first_name, 
                last_name=last_name,
            )
            user.save()
            login(request, user)
            messages.success(request, 'Signed up successfully.')
            return redirect('index')
        except Exception as e:
            messages.error(request, 'An error occurred during signup. Please try again.')
            return render(request, 'authentication/register.html')
            
    return render(request, 'authentication/register.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login  successfully.')
            
            if user.is_admin:
                return redirect("admin_dashboard")
            elif user.is_teacher:
                return redirect("teacher_dashboard")    
            elif user.is_student:
                return redirect("student_dashboard")
            else:
                messages.error(request, 'Invalid User role.')
                return redirect('index')
        else:
            messages.error(request, 'Invalid Credentials.')
    return render(request, 'authentication/login.html')

def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        user = User.objects.filter(email=email).first()

        if user:
            reset_request = PasswordResetRequest.objects.create(
                user=user,
                email=email
            )
            reset_request.send_reset_email(request)
            messages.success(request, 'Password reset email sent. Please check your inbox.')
        else:
            messages.error(request, 'No user found with the provided email.')
    return render(request, 'authentication/forgot-password.html')
    
def reset_password_view(request, token):
    reset_request = PasswordResetRequest.objects.filter(token=token).first()

    if not reset_request or not reset_request.is_valid():
        messages.error(request, 'Invalid or expired password reset token.')
        return redirect('index')

    if request.method == 'POST':
        new_password = request.POST['new_password']
        reset_request.user.set_password(new_password)
        reset_request.user.save()
        messages.success(request, 'Password has been reset successfully.')
        return redirect('login')
    
    return render(request, 'authentication/reset-password.html', {'token': token})
    
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('index')