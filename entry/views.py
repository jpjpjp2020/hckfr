from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import EmployerRegForm, OversightRegform, UserLoginForm
from django.contrib import messages
from django_ratelimit.decorators import ratelimit

# home view

def home(request):
    return render(request, 'landing/landing.html')

# registration views

@ratelimit(key='post:email', method='POST', rate='12/m')
def employer_register(request):
    if request.method == 'POST':
            form = EmployerRegForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.role = 'employer' 
                user.set_password(form.cleaned_data.get('password'))
                user.save()

                messages.success(request, 'Account successfully created. You can sign in now.')
                return redirect('entry:employer_login')
    else:
        form = EmployerRegForm(initial={'role': 'employer'})
    return render(request, 'registration/employer_register.html', {'form': form})

@ratelimit(key='post:email', method='POST', rate='12/m')
def oversight_register(request):
    if request.method == 'POST':
        form = OversightRegform(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'oversight'
            user.set_password(form.cleaned_data.get('password'))
            user.save()

            messages.success(request, 'Account successfully created. You can sign in now.')
            return redirect('entry:oversight_login')
    else:
        form = OversightRegform(initial={'role': 'oversight'})
    return render(request, 'registration/oversight_register.html', {'form': form})

# login views

@ratelimit(key='post:email', method='POST', rate='12/m')
def employer_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.role == 'employer':
                return redirect('feedback:employer_dashboard')
        else:
            messages.error(request, "Login failed. Please check your credentials.")
    else:
        form = UserLoginForm()
    return render(request, 'login/employer_login.html', {'form': form})

@ratelimit(key='post:email', method='POST', rate='12/m')
def oversight_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.role == 'oversight':
                return redirect('feedback:oversight_dashboard')
        else:
            messages.error(request, "Login failed. Please check your credentials.")
    else:
        form = UserLoginForm()
    return render(request, 'login/oversight_login.html', {'form': form})

