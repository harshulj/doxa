#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "doxa.settings")
	from haystack import site
	from polls_and_opinions.models import Poll

	for p in Poll.objects.all():
		for r in p.rating.get_ratings():
			print "%s,%s,%s" % (r.user.id, p.id, r.score)