from django.urls import path
from . import views

app_name = 'feedback'

urlpatterns = [
    path('wdashboard/', views.worker_dashboard, name='worker_dashboard'),
    path('edashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('odashboard/', views.oversight_dashboard, name='oversight_dashboard'),
]