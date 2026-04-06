from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from django.contrib.auth.models import User
from .models import Customer
from .email_utils import send_verification_email, verify_email_token, activate_user_account

class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
        'placeholder': 'Username or Email'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
        'placeholder': 'Password'
    }))

def user_login(request):
    """Smart login view - redirects based on user type"""
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Try to authenticate
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
                
                # Smart redirect based on user type
                if user.is_staff or user.is_superuser:
                    return redirect('admin_dashboard')  # Admin → Admin Dashboard
                else:
                    return redirect('home')            # Regular User → Home Page
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    
    return render(request, 'store/auth/login.html', {'form': form})

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
        'placeholder': 'Enter password'
    }))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
        'placeholder': 'Confirm password'
    }))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': 'Choose username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': 'Enter email address'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': 'First name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': 'Last name'
            }),
        }
    
    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords don't match")
        return password_confirm

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['address', 'city', 'state', 'pincode']
        widgets = {
            'address': forms.Textarea(attrs={
                'rows': 3,
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': 'Street address'
            }),
            'city': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': 'City'
            }),
            'state': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': 'State'
            }),
            'pincode': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': 'PIN code'
            }),
        }

def user_register(request):
    """User registration with email verification"""
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        customer_form = CustomerProfileForm(request.POST)
        
        if user_form.is_valid() and customer_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.is_active = False  # User will be activated after email verification
            user.save()
            
            # Create customer profile
            customer = customer_form.save(commit=False)
            customer.user = user
            customer.save()
            
            # Send verification email
            if send_verification_email(user):
                messages.success(request, 'Registration successful! A verification email has been sent to your email address. Please verify your account before logging in.')
            else:
                messages.error(request, 'Registration successful but failed to send verification email. Please contact support.')
            
            return redirect('verification_sent')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = UserRegistrationForm()
        customer_form = CustomerProfileForm()
    
    return render(request, 'store/auth/register.html', {
        'user_form': user_form,
        'customer_form': customer_form,
    })

def verify_email(request, uidb64, token):
    """Verify email using the link sent to user"""
    user = verify_email_token(uidb64, token)
    
    if user is not None:
        # Activate the user account
        user.is_active = True
        user.save()
        
        # Create customer profile if it doesn't exist
        try:
            customer = user.customer
        except Customer.DoesNotExist:
            customer = Customer.objects.create(user=user)
        
        messages.success(request, 'Your email has been verified! You can now login to your account.')
        return redirect('login')
    else:
        messages.error(request, 'The verification link is invalid or has expired.')
        return redirect('login')

def verification_sent(request):
    """Page shown after registration to instruct user to verify email"""
    return render(request, 'store/auth/verification_sent.html')

def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

@login_required
def user_dashboard(request):
    try:
        customer = request.user.customer
    except Customer.DoesNotExist:
        customer = Customer.objects.create(user=request.user)
    
    return render(request, 'store/auth/dashboard.html', {
        'customer': customer
    })

@login_required
def user_profile(request):
    try:
        customer = request.user.customer
    except Customer.DoesNotExist:
        customer = Customer.objects.create(user=request.user)
    
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST, instance=request.user)
        customer_form = CustomerProfileForm(request.POST, instance=customer)
        
        if user_form.is_valid() and customer_form.is_valid():
            user_form.save()
            customer_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('user_dashboard')
    else:
        user_form = UserRegistrationForm(instance=request.user)
        customer_form = CustomerProfileForm(instance=customer)
    
    return render(request, 'store/profile.html', {
        'user_form': user_form,
        'customer_form': customer_form
    })
