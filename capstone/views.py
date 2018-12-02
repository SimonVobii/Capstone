from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse

def home(request):
	return render(request, 'index.html')

class homeView(TemplateView):
	template_name = "index.html"
