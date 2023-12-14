from django.shortcuts import render


def worker_dashboard(request):
    return render(request, 'feedback/worker_dashboard.html')


def employer_dashboard(request):
    return render(request, 'feedback/employer_dashboard.html')


def oversight_dashboard(request):
    return render(request, 'feedback/oversight_dashboard.html')