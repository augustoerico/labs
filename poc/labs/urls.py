from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
	url(r'^login/$', views.login_form, name='login'),
	url(r'^login/submit/$', views.login_submit, name='login_submit'),
	url(r'^logout/submit/$', views.logout_submit, name='logout_submit'),
    url(r'^projects/(?P<pk>[0-9]+)/$', views.project_detail, name='project_detail'),
	url(r'^projects/create/$', views.project_create, name='project_create'),
	url(r'^projects/(?P<pk>[0-9]+)/budget/create/$', views.budget_create, name='budget_create'),
	url(r'^projects/(?P<pk>[0-9]+)/budgets/edit/$', views.budgets_edit, name='budgets_edit'),
	url(r'^projects/accounts/create/$', views.account_create, name="account_create"),
	url(r'^projects/(?P<username>.+)/report/$', views.generate_report, name="report"),
]
