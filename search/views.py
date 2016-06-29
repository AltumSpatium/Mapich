from django.shortcuts import render, render_to_response
from models import SearchResult
from crawler import query as q, database, crawler
import json, time


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
    full_query = cut_query = requested_query
    if len(cut_query) > 70:
        cut_query = requested_query[:71] + "..."
    return render(request, 'results.html', {'results': results,
                                            'full_query': full_query,
                                            'cut_query': cut_query})


def urls(request):
    all_urls = [url[0] for url in database.get_urls()]
    return render(request, 'urls.html', {'urls': all_urls})


def settings(request):
    settings = {}
    new_settings = request.GET.get('settings', None)
    if new_settings:
        new_settings = new_settings.split(',')
        for setting in new_settings:
            setting = setting.split(':')
            settings[setting[0]] = setting[1]
        with open('search/static/settings/settings.json', 'w') as f:
            f.write(json.dumps(settings))
    else:
        with open('search/static/settings/settings.json', 'r') as f:
            settings = json.loads(f.read())
    return render(request, 'settings.html', {'depth': settings.get("depth")})


def index(request):
    t = None
    indexed_url = request.GET.get('request', None)
    if indexed_url:
        ts = time.time()
        with open('search/static/settings/settings.json', 'r') as f:
            depth = int(json.loads(f.read()).get("depth"))
        c = crawler.Crawler(indexed_url, depth)
        c.crawl()
        t = time.time() - ts
    return render(request, 'index.html', {'time': t})
