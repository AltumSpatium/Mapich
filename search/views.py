from django.shortcuts import render
from models import SearchResult

def index(request):
	return render(request, 'index.html', {})

def results(request):
	query = request.GET['request']
	results = SearchResult.objects.all()
	return render(request, 'results.html', {'results': results, 'query': query})

def urls(request):
	return render(request, 'urls.html', {})

def settings(request):
	return render(request, 'settings.html', {})