from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import UserRegForm, UserLoginForm

# import unified forms above
# define the logic WITH USER ROLES for action:

# home view

def home(request):
    return render(request, 'landing/landing.html')

# registration views

def worker_register(request):
    if request.method == 'POST':
        form = UserRegForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'worker'  # Set the role to branch from unified
            user.set_password(form.cleaned_data.get('password'))
            user.save()

            return redirect('entry:worker_login')
    else:
        form = UserRegForm(initial={'role': 'worker'})
    return render(request, 'registration/worker_register.html', {'form': form})


def employer_register(request):
    if request.method == 'POST':
            form = UserRegForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.role = 'employer' 
                user.set_password(form.cleaned_data.get('password'))
                user.save()

                return redirect('entry:employer_login')
    else:
        form = UserRegForm(initial={'role': 'employer'})
    return render(request, 'registration/employer_register.html', {'form': form})


def oversight_register(request):
    if request.method == 'POST':
            form = UserRegForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.role = 'oversight' 
                user.set_password(form.cleaned_data.get('password'))
                user.save()

                return redirect('entry:oversight_login')
    else:
        form = UserRegForm(initial={'role': 'oversight'})
    return render(request, 'registration/oversight_register.html', {'form': form})


# login views

def worker_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # redirect to feedback dashboards
                if user.role == 'worker':
                    return redirect('feedback:worker_dashboard')
            else:
                form.add_error(None, "Invalid username or password.")
    else:
        form = UserLoginForm()
    return render(request, 'login/worker_login.html', {'form': form})


def employer_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # redirect to feedback dashboards
                if user.role == 'employer':
                    return redirect('feedback:employer_dashboard')
            else:
                form.add_error(None, "Invalid username or password.")
    else:
        form = UserLoginForm()
    return render(request, 'login/employer_login.html', {'form': form})



def oversight_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # redirect to feedback dashboards
                if user.role == 'oversight':
                    return redirect('feedback:oversight_dashboard')
            else:
                form.add_error(None, "Invalid username or password.")
    else:
        form = UserLoginForm()
    return render(request, 'login/oversight_login.html', {'form': form})