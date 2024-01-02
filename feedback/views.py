from django.shortcuts import render
# custom
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.views import View
from entry.decorators import role_required

# std views - USE CLASS BASED VIEWS!!!!!!!!!! but can have both FBVs and CBVs in the same project!!!
# can refactor dashboards into CBVs for modularity and element injection

@role_required('worker', redirect_url='entry:worker_login')
def worker_dashboard(request):
    return render(request, 'dashboard/worker_dashboard.html')

@role_required('employer', redirect_url='entry:employer_login')
def employer_dashboard(request):
    return render(request, 'dashboard/employer_dashboard.html')

@role_required('oversight', redirect_url='entry:oversight_login')
def oversight_dashboard(request):
    return render(request, 'dashboard/oversight_dashboard.html')

# custom

class CustomLogoutView(View):
    def post(self, request, *args, **kwargs):
        logout(request)
        # if needed - branch conditionally
        return HttpResponseRedirect('/')
    
# employer dashboard tools
    
@role_required('employer', redirect_url='entry:employer_login')
def new_feedback_round(request):
    return render(request, 'initial/new_feedback_round.html')

@role_required('employer', redirect_url='entry:employer_login')
def all_active_rounds(request):
    return render(request, 'active/all_active_rounds.html')

@role_required('employer', redirect_url='entry:employer_login')
def employer_guides(request):
    return render(request, 'guides/employer_guides.html')