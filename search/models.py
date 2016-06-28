from __future__ import unicode_literals

from django.db import models


class SearchResult(models.Model):
    site_title = models.CharField(max_length=70)
    site_link = models.CharField(max_length=200)

    def __str__(self):
        return self.site_title


class Index(models.Model):
    url = models.CharField(max_length=200)
    positions = models.TextField()
    title = models.CharField(max_length=70)

    class Meta:
    	verbose_name = 'Index'
    	verbose_name_plural = 'Indexes'

    def __str__(self):
        return self.url


class InvertedIndex(models.Model):
    word = models.CharField(max_length=30)
    url = models.CharField(max_length=200)
    position = models.TextField()

    class Meta:
    	verbose_name = 'Inverted index'
    	verbose_name_plural = 'Inverted indexes'

    def __str__(self):
        return self.word
