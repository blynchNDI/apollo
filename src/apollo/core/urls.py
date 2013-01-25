from django.conf.urls.defaults import *
from tastypie.api import Api
from .api import *
from .views import *

v2_api = Api(api_name='v2')

v2_api.register(ContactResource())
v2_api.register(MessageLogResource())
v2_api.register(LocationResource())
v2_api.register(LocationTypeResource())
v2_api.register(PartnerResource())
v2_api.register(RoleResource())
v2_api.register(FormResource())
v2_api.register(FormGroupResource())
v2_api.register(SubmissionResource())


urlpatterns = patterns('',
    url(r'^$', DashboardView.as_view(), name='dashboard'),
    url(r'^api/', include(v2_api.urls)),
    url(r'^submissions/(?P<form>\d+)/?$', SubmissionListView.as_view(), name='submissions_list'),
    url(r'^submissions/(?P<form>\d+)/export/?$', SubmissionListExportView.as_view(collection='observers'), name='submissions_list_export_observers'),
    url(r'^submissions/(?P<form>\d+)/export/master/?$', SubmissionListExportView.as_view(collection='master'), name='submissions_list_export_master'),
    url(r'^submission/(?P<pk>\d+)/?$', SubmissionEditView.as_view(), name='submission_edit'),
    url(r'^submissions/analysis/(?P<form>\d+)/?$', SubmissionAnalysisView.as_view(), name='submissions_analysis'),
    url(r'^contacts/?$', ContactListView.as_view(), name='contacts_list'),
    url(r'^contact/(?P<pk>\d+)/?$', ContactEditView.as_view(), name='contact_edit'),
    url(r'^tpl/(?P<template_name>.+)/?$', TemplatePreview.as_view()),
)

# authentication urls
urlpatterns += patterns('',
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'core/login.html'}, name="user-login"),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login', name="user-logout")
)