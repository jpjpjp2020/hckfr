from django.urls import path
from . import views

app_name = 'entry'

urlpatterns = [
    # home page as entry point
    path('', views.home, name='home'),
    # reg urls -> views
    # path('wregister/', views.worker_register, name='worker_register'),
    path('eregister/', views.employer_register, name='employer_register'),
    # path('oregister/', views.oversight_register, name='oversight_register'),
    # login urls -> views
    # path('wlogin/', views.worker_login, name='worker_login'),
    path('elogin/', views.employer_login, name='employer_login'),
    # path('ologin/', views.oversight_login, name='oversight_login'),
]