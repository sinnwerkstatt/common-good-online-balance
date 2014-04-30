# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.decorators import login_required

from ecg_balancing.views import *

admin.autodiscover()


urlpatterns = patterns('',

	(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'ecg_balancing/login.html'}),
	(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'template_name': 'ecg_balancing/logout.html'}),

    # url(r'^url/', YourView.as_view()),
    #url(r'^balance$', BalanceMatrixView.as_view(), name='balance'),
    #url(r'^balance$', BalanceMatrixView.as_view(), name='balance'),

	url(r'^companies$', CompanyListView.as_view(), name='companies'),
	url(r'^profile$', login_required(UserDetailView.as_view()), name='profile'),
	url(r'^profile/update$', login_required(UserUpdateView.as_view()), name='update-profile'),
	url(r'^company/(?P<pk>.*?)/update$', login_required(CompanyUpdateView.as_view()), name='update-company'),
	url(r'^company/(?P<pk>.*?)$', login_required(CompanyDetailView.as_view()), name='company'),
	url(r'^balance/create$', login_required(CompanyBalanceCreateView.as_view()), name='create-balance'),
	url(r'^balance/(?P<pk>.*?)/update$', login_required(CompanyBalanceUpdateView.as_view()), name='update-balance'),
	url(r'^balance/(?P<pk>.*?)$', login_required(CompanyBalanceDetailView.as_view()), name='balance'),
	url(r'^indicator/create$', login_required(CompanyBalanceIndicatorCreateView.as_view()), name='create-indicator'),
	url(r'^indicator/(?P<pk>.*?)/update$', login_required(CompanyBalanceIndicatorUpdateView.as_view()), name='update-indicator'),
	url(r'^indicator/(?P<pk>.*?)$', login_required(CompanyBalanceIndicatorDetailView.as_view()), name='indicator'),

    # leave at the end
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('cms.urls')),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
