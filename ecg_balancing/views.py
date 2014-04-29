# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.utils.translation import ungettext, ugettext_lazy as _
from django.views.generic import CreateView, DetailView, UpdateView, ListView
from django.contrib.auth.models import User

from ecg_balancing.models import *

class CompanyListView(ListView):
	model = Company

class UserDetailView(DetailView):
	model = User

class UserUpdateView(UpdateView):
	model = User

class CompanyDetailView(DetailView):
	model = Company

class CompanyUpdateView(UpdateView):
	model = Company

class CompanyBalanceDetailView(DetailView):
	model = CompanyBalance

class CompanyBalanceCreateView(CreateView):
	model = CompanyBalance

class CompanyBalanceUpdateView(UpdateView):
	model = CompanyBalance

class CompanyBalanceIndicatorDetailView(DetailView):
	model = CompanyBalanceIndicator

class CompanyBalanceIndicatorCreateView(CreateView):
	model = CompanyBalanceIndicator

class CompanyBalanceIndicatorUpdateView(UpdateView):
	model = CompanyBalanceIndicator

