from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse

#Simon's Code
"""
class index(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context
"""

def home(request):
	return render(request, 'index.html')

class homeView(TemplateView):
	template_name = "index.html"
