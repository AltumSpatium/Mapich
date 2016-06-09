from __future__ import unicode_literals

from django.db import models

class SearchResult(models.Model):
	site_title = models.CharField(max_length = 70)
	site_link = models.CharField(max_length = 200)

	def __str__(self):
		return self.site_title