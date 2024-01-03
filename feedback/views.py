from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import FeedbackRoundForm, CodeCheckerForm, FeedbackForm
from .models import FeedbackRound, Feedback
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.views import View
from entry.decorators import role_required
from django.utils import timezone


# later can refactor dashboards into CBVs for modularity and element injection

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
    
# new Feedback round view
@role_required('employer', redirect_url='entry:employer_login')
def new_feedback_round(request):
    print("New feedback round view was called with method:", request.method)  # debug
    if request.method == 'POST':
        form = FeedbackRoundForm(request.POST)
        if form.is_valid():
            feedback_round = form.save(commit=False)
            feedback_round.employer = request.user  # employer set to the current user
            if FeedbackRound.can_initiate_new_round(request.user.id):
                feedback_round.save()
                messages.success(request, 'New feedback round created successfully.')
                return redirect('feedback:all_active_rounds')
            else:
                messages.error(request, 'Cannot create a new feedback round at this time - Another round is still accepting feedback.')
                print("Cannot create a new round due to active send window.")  # debug
        else:
            print("Form is not valid:", form.errors)  # debug
    else:
        form = FeedbackRoundForm()

    return render(request, 'initial/new_feedback_round.html', {'form': form})

# All Active Feedback Rounds
@role_required('employer', redirect_url='entry:employer_login')
def all_active_rounds(request):
    active_rounds = FeedbackRound.objects.filter(employer=request.user, feedback_send_window_end__gte=timezone.now())
    return render(request, 'active/all_active_rounds.html', {'active_rounds': active_rounds})

# Round specific page
@role_required('employer', redirect_url='entry:employer_login')
def round_details(request, round_code):
    feedback_round = get_object_or_404(FeedbackRound, feedback_round_code=round_code)
    feedbacks = Feedback.objects.filter(round=feedback_round)
    return render(request, 'active/round_details.html', {'feedback_round': feedback_round, 'feedbacks': feedbacks})

# emploter guides and FAQ
@role_required('employer', redirect_url='entry:employer_login')
def employer_guides(request):
    return render(request, 'guides/employer_guides.html')

# worker dashoard tools

# code checker
@role_required('worker', redirect_url='entry:worker_login')
def worker_code_checker(request):
    print("Codechecker view was called:", request.method)  # debug
    context = {'form': CodeCheckerForm(), 'round': None, 'errors': None}
    if request.method == 'POST':
        form = CodeCheckerForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            print("Form is valid")  # debug
            print("Code:", code)  # debug
            try:
                feedback_round = FeedbackRound.objects.get(feedback_round_code=code, feedback_send_window_end__gt=timezone.now())
                print("Accessing try")  # debug
                print("Print feedbak round:", feedback_round)  # debug
                context['feedback_round'] = feedback_round
                print("Context test:", context)  # debug
            except FeedbackRound.DoesNotExist:
                print("Accessing except")  # debug
                print("No active feedback round found.")  # debug
                context['errors'] = 'No active feedback round found for the provided code.'
            print("Context before rendering:", context)  # debug
        else:
            print("Form is not valid:", form.errors)  # debug
            context['errors'] = 'Please enter a valid code.'
    else:
        form = CodeCheckerForm()

    context['form'] = form
    context['errors'] = context.get('errors', None)

    return render(request, 'active/worker_code_checker.html', context)

# write feedback and drafts
@role_required('worker', redirect_url='entry:worker_login')
def worker_write_feedback(request, round_code=None):
    context = {'form': None, 'round_code': round_code}
    if round_code:
        try:
            feedback_round = FeedbackRound.objects.get(feedback_round_code=round_code, feedback_send_window_end__gt=timezone.now())
            context['feedback_round'] = feedback_round
        except FeedbackRound.DoesNotExist:
            return redirect('error_page')  # NEEDS error handling
    if request.method == 'POST':
        # Handle form submission
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.round = feedback_round
            feedback.sender = request.user
            feedback.receiver = feedback_round.employer
            feedback.is_draft = True  # for draft
            # feedback.encrypt_feedback()
            feedback.save()
    else:
        form = FeedbackForm()
    context['form'] = form
    return render(request, 'initial/worker_write_feedback.html', context)  # {'form': form, 'round_code': round_code}

# worker guides and FAQ
@role_required('worker', redirect_url='entry:worker_login')
def worker_guides(request):
    return render(request, 'guides/worker_guides.html')