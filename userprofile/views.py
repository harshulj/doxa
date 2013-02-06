from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render

from userprofile.models import UserProfile, ProfilePic
from userprofile.forms import UserProfileForm

@login_required
def my_profile(request, template="userprofile/my_profile.html"):
	profile = get_object_or_404(UserProfile, user=request.user)
	return render_to_response(template, { 'profile': profile}, context_instance=RequestContext(request))

@login_required
def edit_profile(request, template="userprofile/edit_profile.html"):
	instance = get_object_or_404(UserProfile, user=request.user)
	if request.method == 'POST':
		form = UserProfileForm(request.POST or None, instance=instance)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('userprofile_my_profile'))
		else:
			return render(request, template, {'form': form}, context_instance=RequestContext(request))
	else:
		form = UserProfileForm(instance=instance)
		return render(request, template, {'form': form}, context_instance=RequestContext(request))
