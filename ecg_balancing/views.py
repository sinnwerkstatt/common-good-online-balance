# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import CreateView, DetailView, UpdateView, ListView, TemplateView
from ecg_balancing.forms import UserProfileForm, CompanyForm

from ecg_balancing.models import *


class CompanyListView(ListView):
    model = Company
    template_name = 'ecg_balancing/companies_list.html'


class UserDetailView(TemplateView):
    template_name = 'ecg_balancing/user_detail.html'


class UserUpdateView(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'ecg_balancing/user_update.html'


class CompanyDetailView(DetailView):
    model = Company


class CompanyUpdateView(UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = 'ecg_balancing/company_update.html'


class CompanyBalanceDetailView(DetailView):
    model = CompanyBalance
    template_name = 'ecg_balancing/company_balance_detail.html'

    def get_object(self, queryset=None):
        # Use a custom queryset if provided; this is required for subclasses
        # like DateDetailView
        if queryset is None:
            queryset = self.get_queryset()

        return queryset.get(company__slug=self.kwargs.get('company_slug'), year=self.kwargs.get('balance_year'))


class CompanyBalanceCreateView(CreateView):
    model = CompanyBalance


class CompanyBalanceUpdateView(UpdateView):
    model = CompanyBalance


class CompanyBalanceIndicatorDetailView(DetailView):
    model = CompanyBalanceIndicator
    template_name = 'ecg_balancing/company_balance_indicator_detail.html'

    def get_context_data(self, **kwargs):
        context = super(CompanyBalanceIndicatorDetailView, self).get_context_data(**kwargs)
        # TODO: simplify the query?
        subindicators = Indicator.objects.filter(parent=self.object.indicator).all().order_by('subindicator_number').all()
        context['subindicators'] = subindicators
        return context

    def get_object(self, queryset=None):
        # Use a custom queryset if provided; this is required for subclasses
        # like DateDetailView
        if queryset is None:
            queryset = self.get_queryset()

        indicatorId = self.kwargs.get('indicator_id')
        indicatorStakeholder = indicatorId[:1]
        indicatorValue = indicatorId[1:]

        return queryset.get(
            company_balance__company__slug=self.kwargs.get('company_slug'),
            company_balance__year=self.kwargs.get('balance_year'),
            indicator__stakeholder=indicatorStakeholder,
            indicator__ecg_value=indicatorValue,
            indicator__parent=None
            )


class CompanyBalanceIndicatorCreateView(CreateView):
    model = CompanyBalanceIndicator


class CompanyBalanceIndicatorUpdateView(UpdateView):
    model = CompanyBalanceIndicator

