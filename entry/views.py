from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import WorkerUserRegForm, EmployerUserRegForm, OversightUserRegForm, WorkerUserLoginForm, EmployerUserLoginForm, OversightUserLoginForm


# registration views

def worker_register(request):
    if request.method == 'POST':
        form = WorkerUserRegForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()

            return redirect('worker_login')
    else:
        form = WorkerUserRegForm()
    return render(request, 'registration/worker_register.html', {'form': form})


def employer_register(request):
    if request.method == 'POST':
            form = EmployerUserRegForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.set_password(user.password)
                user.save()

                return redirect('employer_login')
    else:
        form = EmployerUserRegForm()
    return render(request, 'registration/employer_register.html', {'form': form})


def oversight_register(request):
    if request.method == 'POST':
            form = OversightUserRegForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.set_password(user.password)
                user.save()

                return redirect('oversight_login')
    else:
        form = OversightUserRegForm()
    return render(request, 'registration/oversight_register.html', {'form': form})


# login views

def worker_login(request):
    if request.method == 'POST':
        form = WorkerUserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('usename')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # redirect to feedback dashboards
                return redirect('feeback:worker_dashbard')
            else:
                form.add_error(None, "Invalid username or password.")
    else:
        form = WorkerUserLoginForm()
    return render(request, 'login/worker_login.html', {'form': form})


def employer_login(request):
    pass


def oversight_login(request):
    pass