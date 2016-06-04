from django.shortcuts import render
from models import SearchResult

def index(request):
	return render(request, 'index.html', {})

def results(request):
	results = SearchResult.objects.all()
	return render(request, 'results.html', {'results': results})

def urls(request):
	return render(request, 'urls.html', {})

def settings(request):
	return render(request, 'settings.html', {})