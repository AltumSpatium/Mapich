from __future__ import unicode_literals

from django.db import models
import crawler

class SearchResult(models.Model):
	site_title = models.CharField(max_length = 70)
	site_link = models.CharField(max_length = 70)
	founded_text = models.TextField(max_length = 256)

	def __str__(self):
		return self.founded_text