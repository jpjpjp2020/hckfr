from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import FeedbackRoundForm, CodeCheckerForm, FeedbackForm
from .models import FeedbackRound, Feedback
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.views import View
from entry.decorators import role_required
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

# later can refactor dashboards into CBVs for modularity and element injection

# worker dashboard
@role_required('worker', redirect_url='entry:worker_login')
def worker_dashboard(request):
    request.session['new_feedback_session'] = False
    draft_feedback = Feedback.objects.filter(author=request.user, is_draft=True).first()
    send_window_open = draft_feedback and draft_feedback.round.feedback_send_window_end > timezone.now()

    if draft_feedback and not send_window_open:
        draft_feedback.delete()
        draft_feedback = None

    has_draft = draft_feedback is not None

    context = {
        'has_draft': has_draft,
        'draft_feedback': draft_feedback,
    }

    return render(request, 'dashboard/worker_dashboard.html', context)



# employer dashboard
@role_required('employer', redirect_url='entry:employer_login')
def employer_dashboard(request):
    return render(request, 'dashboard/employer_dashboard.html')

# oversight dashboard
@role_required('oversight', redirect_url='entry:oversight_login')
def oversight_dashboard(request):
    return render(request, 'dashboard/oversight_dashboard.html')

# custom

class CustomLogoutView(View):
    def post(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect('/')
    
# employer dashboard tools
    
# new Feedback round view
@role_required('employer', redirect_url='entry:employer_login')
def new_feedback_round(request):
    if request.method == 'POST':
        form = FeedbackRoundForm(request.POST)
        if form.is_valid():
            feedback_round = form.save(commit=False)
            feedback_round.employer = request.user
            if FeedbackRound.can_initiate_new_round(request.user.id):
                feedback_round.save()
                messages.success(request, 'New feedback round created successfully.')
                return redirect('feedback:all_active_rounds')
            else:
                messages.error(request, 'Cannot create a new feedback round at this time - Another round is still accepting feedback.')
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
    context = {'form': CodeCheckerForm(), 'round': None, 'errors': None}
    if request.method == 'POST':
        form = CodeCheckerForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                feedback_round = FeedbackRound.objects.get(feedback_round_code=code, feedback_send_window_end__gt=timezone.now())
                context['feedback_round'] = feedback_round
            except FeedbackRound.DoesNotExist:
                context['errors'] = 'No active feedback round found for the provided code.'
        else:
            context['errors'] = 'Please enter a valid code.'
    else:
        form = CodeCheckerForm()

    context['form'] = form
    context['errors'] = context.get('errors', None)

    return render(request, 'active/worker_code_checker.html', context)

# Initialize feedback | reuse CodeCheckerForm - rework split view initilizattion part too
@role_required('worker', redirect_url='entry:worker_login')
def worker_input_code(request):
    form = CodeCheckerForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        code = form.cleaned_data.get('code')
        try:
            feedback_round = FeedbackRound.objects.get(feedback_round_code=code)
            return redirect('feedback:worker_write_feedback', round_code=code)
        except FeedbackRound.DoesNotExist:
            form.add_error('code', 'Invalid code. Please try again.')

    context = {'form': form}
    return render(request, 'initial/worker_input_code.html', context)

# write feedback
@role_required('worker', redirect_url='entry:worker_login')
def worker_write_feedback(request, round_code):
    context = {'round_code': round_code}
    feedback_round = get_object_or_404(FeedbackRound, feedback_round_code=round_code)
    send_window_open = feedback_round.feedback_send_window_end > timezone.now()
    
    if not send_window_open:
        messages.info(request, 'The sending time for this feedback round is over.')
        return redirect('feedback:worker_dashboard')
    
    if Feedback.objects.filter(round=feedback_round, author=request.user, is_draft=False).exists():
        messages.info(request, 'You have already sent feedback for this round.')
        return redirect('feedback:worker_dashboard')

    new_feedback_session = request.session.get('new_feedback_session', False)

    draft_feedback = Feedback.objects.filter(round=feedback_round, author=request.user, is_draft=True).first()
    if draft_feedback and not new_feedback_session:
        return redirect('feedback:worker_edit_feedback', round_code=round_code)

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():

            draft_feedback = Feedback.objects.filter(round=feedback_round, author=request.user, is_draft=True).first()
            
            if draft_feedback:
                feedback = form.save(commit=False)
                draft_feedback.title = feedback.title
                draft_feedback.content = feedback.content
                draft_feedback.save()
                feedback = draft_feedback
            else:
                feedback = form.save(commit=False)
                feedback.round = feedback_round
                feedback.author = request.user
                feedback.receiver = feedback_round.employer
                feedback.is_draft = True
                feedback.save()

            if request.POST.get('save-button') == 'save':
                request.session['new_feedback_session'] = True  # session variable
                messages.success(request, 'Draft saved successfully.')
                # stay with current form
                form = FeedbackForm(instance=feedback)
                context['form'] = form
                return render(request, 'initial/worker_write_feedback.html', context)
            elif request.POST.get('send-button') == 'send':
                feedback.is_draft = False
                feedback.save()
                request.session['new_feedback_session'] = False
                messages.success(request, 'Feedback sent successfully.')
                return redirect('feedback:worker_dashboard')
    else:
        form = FeedbackForm()
        request.session['new_feedback_session'] = True  # session variable

    context['form'] = form
    return render(request, 'initial/worker_write_feedback.html', context)


# edit feedback
@role_required('worker', redirect_url='entry:worker_login')
def worker_edit_feedback(request, round_code):
    feedback_round = get_object_or_404(FeedbackRound, feedback_round_code=round_code)
    draft_feedback = get_object_or_404(Feedback, round=feedback_round, author=request.user, is_draft=True)

    context = {'round_code': round_code}
    
    if request.method == 'POST':
        form = FeedbackForm(request.POST, instance=draft_feedback)
        if form.is_valid():
            feedback = form.save(commit=False)
            if 'save' in request.POST:
                feedback.save()
                messages.success(request, 'Draft updated successfully.')
                context['form'] = form
                return render(request, 'initial/worker_edit_feedback.html', context)
            elif 'send' in request.POST:
                feedback.is_draft = False
                feedback.save()
                messages.success(request, 'Feedback sent successfully.')
                return redirect('feedback:worker_dashboard')
    else:
        form = FeedbackForm(instance=draft_feedback)
        context['form'] = form

    return render(request, 'initial/worker_edit_feedback.html', context)

# worker guides and FAQ
@role_required('worker', redirect_url='entry:worker_login')
def worker_guides(request):
    return render(request, 'guides/worker_guides.html')
