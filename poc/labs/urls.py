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
]
