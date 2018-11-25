from django.shortcuts import render, redirect
from django.views.generic import FormView, CreateView
from django.contrib.auth.models import User
from .forms import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect('survey')
    else:
        form = UserRegisterForm()
    return render(request, 'register_paul.html', {'form': form})

@login_required
def survey(request):
    if request.method == 'POST':
        survey_form = SurveySubmissionForm(request.POST)
        if survey_form.is_valid():
            save_it = survey_form.save(commit = False)
            save_it.user = request.user
            save_it .save()
            messages.success(request, f'Questionnaire Data Saved')
            return redirect('select')
        else:
            messages.error(request, "Error Submitting Questionnaire")
    else:
        survey_form = SurveySubmissionForm()
    return render(request, 'questionaires_paul.html', {'form': survey_form})

"""
class surveyView(CreateView):
    template_name = 'questionaires_paul.html'
    fields = ['age','gender','status','investment','combination']

    def form_valid(self, form):
        form.instance.userID = self.request.user
        return super().form_valid(form)
"""

    # Simon's default code
"""
class LoginView(FormView):

    form_class = LoginForm
    template_name = 'account/login.html'

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)

    def form_invalid(self, form, **kwargs):
        kwargs.update({'form': form})
        return self.render_to_response(self.get_context_data(**kwargs))

    def get_success_url(self):
       return self.request.POST.get('next', reverse('index'))
"""
