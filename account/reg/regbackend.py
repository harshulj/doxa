from account.reg.forms import UserRegistrationForm

def post_user_create(sender, user, request, **kwargs):
	user.first_name = request.POST["first_name"]
	user.last_name = request.POST["last_name"]
	user.save()

from registration.signals import user_registered
user_registered.connect(post_user_create)
