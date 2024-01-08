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
    # employer round specific conditional page
    path('edashboard/round_details/<str:round_code>/', views.round_details, name='round_details'),
    # worker tools
    path('wdashboard/code_checker/', views.worker_code_checker, name='worker_code_checker'),
    path('wdashboard/write_feedback/<str:round_code>', views.worker_write_feedback, name='worker_write_feedback'),
    path('wdashboard/edit_feedback/<str:round_code>/', views.worker_edit_feedback, name='worker_edit_feedback'),
    path('wdashboard/input_code/', views.worker_input_code, name='worker_input_code'),
    path('wdashboard/guides/', views.worker_guides, name='worker_guides'),
    # oversight tools
    path('odashboard/active_rounds/<int:employer_id>/', views.oversight_employer_rounds, name='oversight_employer_rounds'),
    path('odashboard/round_details/<str:round_code>/', views.oversight_feedback_in_employer_rounds, name='oversight_feedback_in_employer_rounds'),
    path('odashboard/guides/', views.oversight_guides, name='oversight_guides'),

]