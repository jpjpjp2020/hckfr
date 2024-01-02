from django.urls import path
from . import views

app_name = 'feedback'

urlpatterns = [
    # dashboards
    path('wdashboard/', views.worker_dashboard, name='worker_dashboard'),
    path('edashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('odashboard/', views.oversight_dashboard, name='oversight_dashboard'),
    # employer tools
    path('edashboard/new_round/', views.new_feedback_round, name='new_feedback_round'),
    path('edashboard/all_rounds/', views.all_active_rounds, name='all_active_rounds'),
    path('edashboard/guides/', views.employer_guides, name='employer_guides'),
    # round specific conditional page
    path('round_details/<str:round_code>/', views.round_details, name='round_details'),
]