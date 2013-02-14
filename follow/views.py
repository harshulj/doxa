from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson as json
from relationships.decorators import require_user
from relationships.views import get_relationship_status_or_404

@login_required
@require_user
def relationship_handler(request, user, status_slug, add=True,template_name='relationships/confirm.html',success_template_name='relationships/success.html'):
	status = get_relationship_status_or_404(status_slug)
	is_symm = status_slug == status.symmetrical_slug
	if request.method == 'POST':
		if add:
			request.user.relationships.add(user, status, is_symm)
		else:
			request.user.relationships.remove(user, status, is_symm)
		if request.is_ajax():
			response = {'result': '1'}
			return HttpResponse(json.dumps(response), mimetype="application/json")
		if request.GET.get('next'):
			return HttpResponseRedirect(request.GET['next'])
		template_name = success_template_name

	return render_to_response(template_name,{'to_user': user, 'status': status, 'add': add},context_instance=RequestContext(request))

