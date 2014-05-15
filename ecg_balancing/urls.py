# -*- coding: utf-8 -*-

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


	url(r'^user/(?P<pk>.*)/$', login_required(UserDetailView.as_view()), name='user-detail'),
	url(r'^user/(?P<pk>.*)/update$', login_required(UserUpdateView.as_view()), name='user-update'),

	url(r'^companies$', CompanyListView.as_view(), name='companies'),
	url(r'^company/(?P<slug>[\w-]*)/$', login_required(CompanyDetailView.as_view()), name='company-detail'),
	url(r'^company/(?P<slug>[\w-]*)/update$', login_required(CompanyUpdateView.as_view()), name='company-update'),

    # Balances: /company/balance_year
	url(r'^company/(?P<company_slug>[\w-]*)/balance/create$', login_required(CompanyBalanceCreateView.as_view()), name='balance-create'),
	url(r'^company/(?P<company_slug>[\w-]*)/(?P<balance_year>[0-9]*)/$', login_required(CompanyBalanceDetailView.as_view()), name='balance-detail'),
	url(r'^company/(?P<company_slug>[\w-]*)/(?P<balance_year>[0-9]*)/update/$', login_required(CompanyBalanceUpdateView.as_view()), name='balance-update'),

    # Indicators: /sinnwerkstatt/2014/c1
	#url(r'^indicator/create$', login_required(CompanyBalanceIndicatorCreateView.as_view()), name='indicator-create'),
	url(r'^company/(?P<company_slug>[\w-]*)/(?P<balance_year>[0-9]*)/(?P<indicator_id>[\w.]*)$', login_required(CompanyBalanceIndicatorDetailView.as_view()), name='indicator-detail'),
	url(r'^company/(?P<company_slug>[\w-]*)/indicator/(?P<pk>[\d]*)/update$', login_required(CompanyBalanceIndicatorUpdateView.as_view()), name='indicator-update'),


    # leave at the end
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()

urlpatterns += patterns('',
    url(r'^', include('cms.urls')),
)
