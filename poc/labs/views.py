from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from labs.models import Responsible, Project, Laboratory, Budget

from decimal import Decimal

@login_required(login_url='/labs/login/') # FIXME put the login_url in settings
def index(request):
	user = request.user
	
	responsible = Responsible.objects.get(username=user.username)
	projects = Project.objects.filter(responsible=responsible)
	laboratories = responsible.laboratory_set.all()
	
	return render(request, 'labs/index.html', 
				  {'user': user, 'projects': projects,
				  'laboratories': laboratories}
				 )

def login_form(request):
	return render(request, 'labs/login.html')

def login_submit(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=username, password=password)
	if user is not None:
		if user.is_active:
			login(request, user)
			# Redirect to a success page.
			return redirect('/labs/') # FIXME don't hard code the URL!
	
	return render(request, 'labs/login.html', 
				  {'error_message': 'Could not authenticate.', }
				 )

def logout_submit(request):
	logout(request)
	return redirect('/labs/login/') # FIXME don't hard code the URL!
	
@login_required(login_url='/labs/login/') # FIXME put the login_url in settings
def project_detail(request, pk):
	project = get_object_or_404(Project, pk=pk)	
	return render(request, 'labs/project_detail.html', 
				 { 'project' : project,
				 'budget' : project.budget_set.all(),}
				 )

@login_required(login_url='/labs/login/') # FIXME
def project_create(request):
	user = request.user
	
	tag = request.POST['tag']
	start_date = request.POST['start_date']
	laboratory_id = request.POST['laboratory']
	
	responsible = Responsible.objects.get(username=user.username)
	laboratory = Laboratory.objects.get(id=laboratory_id)
	
	responsible.project_set.create(laboratory=laboratory, tag=tag, start_date=start_date)
	
	return redirect('/labs/') # FIXME

@login_required(login_url='/labs/login/') # FIXME
def budget_create(request, pk):
	
	value = request.POST['value']
	in_date = request.POST['in_date']
	
	project = Project.objects.get(pk=pk)
	project.budget_set.create(value=Decimal(value), in_date=in_date)
	
	return redirect(reverse('labs:project_detail', args=(pk,)))