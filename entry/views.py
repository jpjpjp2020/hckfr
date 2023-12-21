from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import UserRegForm, UserLoginForm
from django.contrib import messages

# home view

def home(request):
    return render(request, 'landing/landing.html')

# registration views

# def worker_register(request):
#     if request.method == 'POST':
#         form = UserRegForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.role = 'worker'  # Set the role to branch from unified
#             user.set_password(form.cleaned_data.get('password'))
#             user.save()

#             messages.success(request, 'Account successfully created. You can sign in now.')
#             return redirect('entry:worker_login')
#     else:
#         form = UserRegForm(initial={'role': 'worker'})
#     return render(request, 'registration/worker_register.html', {'form': form})


def employer_register(request):
    if request.method == 'POST':
            form = UserRegForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.role = 'employer' 
                user.set_password(form.cleaned_data.get('password'))
                user.save()

                messages.success(request, 'Account successfully created. You can sign in now.')
                return redirect('entry:employer_login')
    else:
        form = UserRegForm(initial={'role': 'employer'})
    return render(request, 'registration/employer_register.html', {'form': form})


# def oversight_register(request):
#     if request.method == 'POST':
#             form = UserRegForm(request.POST)
#             if form.is_valid():
#                 user = form.save(commit=False)
#                 user.role = 'oversight' 
#                 user.set_password(form.cleaned_data.get('password'))
#                 user.save()

#                 messages.success(request, 'Account successfully created. You can sign in now.')
#                 return redirect('entry:oversight_login')
#     else:
#         form = UserRegForm(initial={'role': 'oversight'})
#     return render(request, 'registration/oversight_register.html', {'form': form})


# login views

# def worker_login(request):
#     if request.method == 'POST':
#         post_data = request.POST.copy()
#         post_data['role'] = 'worker'

#         form = UserLoginForm(post_data)
#         print("POST data:", request.POST)
#         print("Modified form data:", post_data)

#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             #debug
#             print("Username:", username)
#             print("Password:", password)
#             print("Calling authenticate...")
#             user = authenticate(username=username, password=password, role='worker')
#             print("Authenticated user:", user)
#             if user is not None:
#                 login(request, user)
#                 return redirect('feedback:worker_dashboard')
#             else:
#                 print("Form errors:", form.errors.as_text())
#                 messages.error(request, "Invalid username or password.")
#         else:
#             print("Form errors immediately after is_valid check:", form.errors)
#             print("Form errors:", form.errors.as_text())
#             print("Form is not valid")
#             print("Form data:", form.data)
#             print("Form is not valid immediately after validation check")
#             print("Form errors:", form.errors)
#             messages.error(request, "Please correct the error below.")
#     else:
#         form = UserLoginForm()
#     return render(request, 'login/worker_login.html', {'form': form})


# update based on the above

def employer_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(email=username, password=password, role='employer')
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



# def oversight_login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(request, data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(email=username, password=password, role='oversight')
#             if user is not None:
#                 login(request, user)
#                 # redirect to feedback dashboards
#                 if user.role == 'oversight':
#                     return redirect('feedback:oversight_dashboard')
#             else:
#                 form.add_error(None, "Invalid username or password.")
#     else:
#         form = UserLoginForm()
#     return render(request, 'login/oversight_login.html', {'form': form})