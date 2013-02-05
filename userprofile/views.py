from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from userprofile.models import UserProfile, ProfilePic

@login_required
def my_profile(request, template="userprofile/my_profile.html"):
	profile = get_object_or_404(UserProfile, user=request.user)
	return render_to_response(template, { 'profile': profile}, context_instance=RequestContext(request))

