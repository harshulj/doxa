from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render

from userprofile.models import UserProfile, ProfilePic
from userprofile.forms import UserProfileForm, ProfilePicForm

@login_required
def my_profile(request, template="userprofile/my_profile.html"):
	"""
		This vie shows a user his own profile.
	"""
	profile = get_object_or_404(UserProfile, user=request.user)
	return render_to_response(template, { 'profile': profile}, context_instance=RequestContext(request))

@login_required
def edit_profile(request, template="userprofile/edit_profile.html"):
	"""
		This view shows the profile form so that a user can edit it.
	"""
	profile_instance = get_object_or_404(UserProfile, user=request.user)
	pic_instance = get_object_or_404(ProfilePic, user=request.user)
	if request.method == 'POST':
		profile_form = UserProfileForm(request.POST or None, instance=profile_instance)
		pic_form = ProfilePicForm(request.POST or None, request.FILES or None, instance=pic_instance)
		if profile_form.is_valid() & pic_form.is_valid():
			profile_form.save()
			pic_form.save()
			return HttpResponseRedirect(reverse('userprofile_my_profile'))
		else:
			return render(request, template, {'form': form}, context_instance=RequestContext(request))
	else:
		profile_form = UserProfileForm(instance=profile_instance)
		pic_form = ProfilePicForm(instance=pic_instance)
		return render(request, template, {'profile_form': profile_form, 'pic_form':pic_form}, context_instance=RequestContext(request))
