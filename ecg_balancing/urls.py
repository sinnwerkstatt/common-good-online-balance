# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.decorators import login_required
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy
from ecg_balancing.forms import UserAccountCreationForm

from ecg_balancing.views import *

admin.autodiscover()


urlpatterns = patterns('',

	url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'ecg_balancing/registration/login.html'}, name='login'),
	url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'template_name': 'ecg_balancing/registration/logout.html'}, name='logout'),
    url(r'^accounts/profile/$', UserDetailRedirect.as_view(url=reverse_lazy('user-detail'))),
    url(r'^accounts/register/$', UserCreateView.as_view(
        template_name='ecg_balancing/registration/register.html', form_class=UserAccountCreationForm, success_url='reverse("user-detail")'), name='register'),

    url(r'^password_reset/$', 'django.contrib.auth.views.password_reset',
        {'template_name': 'ecg_balancing/registration/password_reset_form.html'}, name='password_reset'),
    url(r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done',
        {'template_name': 'ecg_balancing/registration/password_reset_done.html'}, name='password_reset_done'),
    url(r'^reset/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 'django.contrib.auth.views.password_reset_confirm',
        {'template_name': 'ecg_balancing/registration/password_reset_confirm.html'}, name='password_reset_confirm'),
    url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete',
        {'template_name': 'ecg_balancing/registration/password_reset_done.html'}, name='password_reset_complete'),

    url(r'^password_change/$', 'django.contrib.auth.views.password_change', {'template_name': 'ecg_balancing/registration/password_change_form.html'}, name='password_change'),
    url(r'^password_change/done/$', 'django.contrib.auth.views.password_change_done', {'template_name': 'ecg_balancing/registration/password_change_done.html'}, name='password_change_done'),


	url(r'^user/(?P<pk>.*)/$', login_required(UserDetailView.as_view()), name='user-detail'),
	url(r'^user/(?P<pk>.*)/update$', login_required(UserUpdateView.as_view()), name='user-update'),

	url(r'^companies$', CompanyListView.as_view(), name='companies'),
	url(r'^company-join/$', login_required(CompanyJoinView.as_view()), name='company-join'),
	url(r'^company-create/$', login_required(CompanyDetailView.as_view()), name='company-create'),

	url(r'^company/(?P<slug>[\w-]*)/$', CompanyDetailView.as_view(), name='company-detail'),
	url(r'^company/(?P<slug>[\w-]*)/update$', login_required(CompanyUpdateView.as_view()), name='company-update'),
	url(r'^company/(?P<slug>[\w-]*)/admin$', login_required(CompanyAdminView.as_view()), name='company-admin'),

    # Balances: /company/balance_year
	url(r'^company/(?P<company_slug>[\w-]*)/balance/create$', login_required(CompanyBalanceCreateView.as_view()), name='balance-create'),
	url(r'^company/(?P<company_slug>[\w-]*)/(?P<balance_year>[0-9]*)/$', login_required(CompanyBalanceDetailView.as_view()), name='balance-detail'),
	url(r'^company/(?P<company_slug>[\w-]*)/(?P<balance_year>[0-9]*)/update/$', login_required(CompanyBalanceUpdateView.as_view()), name='balance-update'),

    # Indicators: /sinnwerkstatt/2014/c1
	#url(r'^indicator/create$', login_required(CompanyBalanceIndicatorCreateView.as_view()), name='indicator-create'),
	url(r'^company/(?P<company_slug>[\w-]*)/(?P<balance_year>[0-9]*)/(?P<indicator_id>[\w.]*)$', login_required(CompanyBalanceIndicatorDetailView.as_view()), name='indicator-detail'),
	url(r'^company/(?P<company_slug>[\w-]*)/indicator/(?P<pk>[\d]*)/update$', login_required(CompanyBalanceIndicatorUpdateView.as_view()), name='indicator-update'),

    url(r'^feedback/indicator/(?P<indicator_id>[\w.]*)$', login_required(FeedbackIndicatorFormView.as_view()), name='feedback-indicator'),
    url(r'^feedback/success/$', login_required(FeedbackIndicatorSuccessView.as_view()), name='feedback-indicator-success'),


    # leave at the end
    url(r'^select2/', include('select2.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()

urlpatterns += patterns('',
    url(r'^', include('cms.urls')),
)
