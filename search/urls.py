from django.conf.urls import url
import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^index.html$', views.index, name='index'),
	url(r'^results.html$', views.results, name='results'),
	url(r'^urls.html$', views.urls, name='urls'),
	url(r'^settings.html$', views.settings, name='settings'),
]