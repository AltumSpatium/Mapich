from django.shortcuts import render, render_to_response
from models import SearchResult
from crawler import query as q, database, crawler


def base(request):
    return render(request, 'base.html', {})


def results(request):
    requested_query = request.GET['request']
    results = []
    query = q.free_query(requested_query)
    ranked_query = q.simple_ranked_results(query)
    urls = {}
    for url in database.get_urls():
        urls[url[0]] = url[1]
    title = ""
    for link in ranked_query:
        if link[0] in urls:
            title = urls[link[0]]
        results.append(SearchResult(site_title=title,
                                    site_link=link[0]))
    return render(request, 'results.html', {'results': results, 'query': requested_query})


def urls(request):
    all_urls = [url[0] for url in database.get_urls()]
    return render(request, 'urls.html', {'urls': all_urls})


def settings(request):
    return render(request, 'settings.html', {})


def index(request):
    try:
        indexed_url = request.GET['request']
        if indexed_url:
            c = crawler.Crawler(indexed_url, 0)  # Add setting to change depth
            c.crawl()
    except:
        pass
    return render(request, 'index.html', {})
