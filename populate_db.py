#!/usr/bin/env python
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "doxa.settings")
def readqs(lines):
	ret = {}
	index = 0
	while index < len(lines):
		#print index, len(lines)
		while index < len(lines) and not lines[index].strip():
			index += 1
		if not index < len(lines):
			break
		key = lines[index].strip()
		index +=1 
		val = []
		while lines[index].strip():
			val.append(lines[index].strip())
			index += 1
		ret[key] = val
	return ret
	
def get_tags(q_text):
	forbidden = ['who','why','when','where','and','because']
	tags = []
	for w in q_text.split():
		if len(w) > 3 and w not in forbidden:
			tags.append(w.lower())
	tags = list(set(tags))		
	
	import random
	sample_sz = len(tags) - 3
	if sample_sz < 0 :
		sample_sz = len(tags)
	return ", ".join(random.sample(tags,sample_sz))
	
def generate_ip():
	ints = []
	for i in xrange(4):
		ints.append(str(random.randint(1,255)))
	return '.'.join(ints)
	
if __name__ == "__main__":
	from haystack import site
	from polls_and_opinions.models import Poll,Choice
	import datetime
	from django.contrib.auth.models import User
	import random
	
	users = User.objects.all()
	
	polls_dict = readqs(open("all","r").readlines())
	
	for k,v in polls_dict.items():
		print "adding %s\n%s" % (k,v)
		auth = users[random.randint(0,len(users)-1)]
		tags = get_tags(k)
		print tags
		p = Poll(question=k,published_on=datetime.datetime.now(), \
				duration=300,is_live=True,author=auth, \
				tags = tags)
		
		sample_sz = 6 if len(users) > 9 else 3
		if len(users) < 3:
			sample_sz = 1
			
		sample = random.sample(users,sample_sz)
		p.save()			
		for u in sample:
			p.rating.add(score=random.randint(1,5), user=u,\
                             ip_address=generate_ip())

		
		for ch_text in v :
			ch = Choice(author=auth, text= ch_text,poll=p,is_approved=True)
			ch.save()
			

