# -*- coding: UTF-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse

from labs.models import Responsible, Project, Laboratory, Budget

from tempfile import NamedTemporaryFile
from decimal import Decimal
import datetime
import json

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
	
	project = responsible.project_set.create(laboratory=laboratory, tag=tag, start_date=start_date)
	
	# Initialize the project budget for 12 months
	# FIXME refactor this
	initial_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
	for m in range(0, 12):
		date = add_months(initial_date, m)
		project.budget_set.create(value=Decimal(0), in_date=date)
	
	return redirect('/labs/') # FIXME

@login_required(login_url='/labs/login/') # FIXME
def budget_create(request, pk):
	
	value = request.POST['value']
	in_date = request.POST['in_date']
	
	project = Project.objects.get(pk=pk)
	project.budget_set.create(value=Decimal(value), in_date=in_date)
	
	return redirect(reverse('labs:project_detail', args=(pk,)))	

@login_required(login_url='/labs/login/') # FIXME
def budgets_edit(request, pk):
	
	form_data = request.POST['budgets']
	form_data = json.loads(form_data)
	
	for d in form_data['data']:
		budget = Budget.objects.get(pk=Decimal(d['id']))
		budget.value = Decimal(d['value'])
		budget.save()
	
	return redirect(reverse('labs:project_detail', args=(pk,)))	

@login_required(login_url='/labs/login/') # FIXME
def generate_report(request, username):
	
	r = Responsible.objects.get(username=username)
	projects = r.project_set.all()
	
	# get the first 12 months since this month
	today = datetime.date.today()
	if today.month > 1:
		month = today.month - 1
		year = today.year
	else:
		month = 12
		year = today.year - 1
		
	reference_date = datetime.date(year, month, 1)
	
	# builds string lines
	# FIXME fix this whole mess...
	out = u'Laboratório,Projeto,Ano,Repsonsável,M1,M2,M3,M4,M5,M6,M7,M8,M9,M10,M11,M12\n'
	for project in projects:
		budgets = project.budget_set.filter(in_date__gte=reference_date)
		values = ','.join([ str(b.value) for b in budgets ])
		line = project.laboratory.tag + ',' + project.tag + ',' + str(project.start_date.year) + ',' + r.username + ',' + values + '\n'
		out += line
	
	response = HttpResponse(content_type='text/plain')
	response['Content-Disposition'] = 'attachment; filename="report.csv"'
	response.write(out)
			
	#return 	HttpResponse(out)
	return response

def account_create(request):
	
	username = request.POST['username']
	email = request.POST['email']
	password = request.POST['password']
	lab = request.POST['lab']
	
	user = User.objects.create_user(username, email, password)
	if user:
		messages.add_message(request, messages.SUCCESS, 'Account created.')
		responsible = Responsible.objects.create(username=username)
		laboratory = Laboratory.objects.get(tag=lab)
		laboratory.responsibles.add(responsible)
		
	else:
		messages.add_message(request, messages.ERROR, 'Failed at account creation.')
	
	return redirect('labs:login')

def add_months(date, months):
	
	month = date.month - 1 + months
	year = date.year + int(month/12)
	month = month%12 + 1
	return datetime.date(year, month, 1)
