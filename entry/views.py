from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import UserRegForm, UserLoginForm
from django.contrib import messages

# home view

def home(request):
    return render(request, 'landing/landing.html')

# registration views

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


# CLEAN ONE
# def employer_login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(request, data=request.POST)
#         if form.is_valid():
#             email = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(email=email, password=password)
#             if user is not None:
#                 login(request, user)
#                 # redirect to feedback dashboards
#                 if user.role == 'employer':
#                     return redirect('feedback:employer_dashboard')
#             else:
#                 form.add_error(None, "Invalid email or password.")
#     else:
#         form = UserLoginForm()
#     return render(request, 'login/employer_login.html', {'form': form})

# TEST ONE:

def employer_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.role == 'employer':
                return redirect('feedback:employer_dashboard')
            # Add any other role-based redirects if necessary
        else:
            print("Form is not valid. Errors:", form.errors)
    else:
        form = UserLoginForm()
    return render(request, 'login/employer_login.html', {'form': form})



# DEBUG ONE
# def employer_login(request):
#     print("Employer login view called with method:", request.method)

#     if request.method == 'POST':
#         form = UserLoginForm(request, data=request.POST)
#         print("Form data received:", request.POST)

#         if form.is_valid():
#             print("Form is valid")
#             email = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             print("Extracted data - Email:", email, "Password:", password)
#             print("About to call authenticate with - Email:", email, "Password:", password)
#             user = authenticate(email=email, password=password)
#             print("User returned from authenticate:", user)

#             if user is not None:
#                 login(request, user)
#                 print("User logged in:", user)
                
#                 if user.role == 'employer':
#                     print("Redirecting to employer dashboard")
#                     return redirect('feedback:employer_dashboard')
#             else:
#                 print("Authentication failed")
#                 form.add_error(None, "Invalid email or password.")
#         else:
#             print("Form is not valid. Errors:", form.errors)
#     else:
#         form = UserLoginForm()
#         print("GET request, rendering empty login form")

#     return render(request, 'login/employer_login.html', {'form': form})
