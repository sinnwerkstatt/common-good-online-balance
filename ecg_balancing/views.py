# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.http import (Http404, HttpResponse, HttpResponseNotFound,
    HttpResponseRedirect, StreamingHttpResponse)
from django.shortcuts import get_object_or_404
from django.utils.translation import ungettext, ugettext_lazy as _
from django.views.generic import (View, TemplateView)


class BalanceMatrixView(TemplateView):

    template_name = 'balance-matrix.html'

    def get_context_data(self, **kwargs):
        context = super(BalanceMatrixView, self).get_context_data(**kwargs)

        context.update({
            'TODOaddsomething': 'tothedashboard'
        })

        return context
