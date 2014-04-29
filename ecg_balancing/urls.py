# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from ecg_balancing.views import BalanceMatrixView

admin.autodiscover()


urlpatterns = patterns('',

    # url(r'^url/', YourView.as_view()),
    url(r'^balance$', BalanceMatrixView.as_view(), name='balance'),

    # leave at the end
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('cms.urls')),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
