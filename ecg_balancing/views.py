# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect

from django.views.generic import CreateView, DetailView, UpdateView, ListView, TemplateView
from ecg_balancing.forms import UserProfileForm, CompanyForm, CompanyBalanceForm, CompanyBalanceEditForm

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

    def get_success_url(self):
        if 'slug' in self.kwargs:
            slug = self.kwargs['slug']
            return reverse('company-detail', kwargs={'slug': slug})
        else:
            return super(CompanyUpdateView, self).get_success_url()


class CompanyBalanceDetailView(DetailView):
    model = CompanyBalance
    template_name = 'ecg_balancing/company_balance_detail.html'

    def get_context_data(self, **kwargs):
        context = super(CompanyBalanceDetailView, self).get_context_data(**kwargs)
        context['indicators'] = self.object.company_balance.filter(indicator__parent=None).order_by('indicator__stakeholder')
        return context

    def get_object(self, queryset=None):
        # Use a custom queryset if provided; this is required for subclasses
        # like DateDetailView
        if queryset is None:
            queryset = self.get_queryset()

        return queryset.get(company__slug=self.kwargs.get('company_slug'), year=self.kwargs.get('balance_year'))


class CompanyBalanceCreateView(CreateView):
    model = CompanyBalance
    template_name = 'ecg_balancing/company_balance_create.html'
    form_class = CompanyBalanceForm

    def get_context_data(self, **kwargs):
        context = super(CompanyBalanceCreateView, self).get_context_data(**kwargs)
        company = Company.objects.get(slug=self.kwargs.get('company_slug'))
        context['company'] = company
        context['form'].fields['company'].initial = company
        return context

    def form_valid(self, form, **kwargs):
        self.object = form.save(commit=False)
        self.object.status = CompanyBalance.STATUS_CHOICE_STARTED
        self.object.save()

        return HttpResponseRedirect(reverse_lazy('balance-detail',
                                                 kwargs={
                                                     'company_slug': self.object.company.slug,
                                                     'balance_year': self.object.year
                                                 }))


class CompanyBalanceUpdateView(UpdateView):
    model = CompanyBalance
    template_name = 'ecg_balancing/company_balance_update.html'
    form_class = CompanyBalanceEditForm

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        return queryset.get(company__slug=self.kwargs.get('company_slug'), year=self.kwargs.get('balance_year'))

    def get_success_url(self):
        return reverse('balance-detail', kwargs={
            'company_slug': self.object.company.slug,
            'balance_year': self.object.year
        })


class CompanyBalanceIndicatorDetailView(DetailView):
    model = CompanyBalanceIndicator
    template_name = 'ecg_balancing/company_balance_indicator_detail.html'

    def get_context_data(self, **kwargs):
        context = super(CompanyBalanceIndicatorDetailView, self).get_context_data(**kwargs)
        # TODO: simplify the query?
        # subindicators = Indicator.objects.filter(parent=self.object.indicator).all().order_by('subindicator_number').all()
        subindicators = CompanyBalanceIndicator.objects.filter(company_balance=self.object.company_balance,
                                                               indicator__parent=self.object.indicator).all().order_by(
            'indicator__subindicator_number').all()
        context['subindicators'] = subindicators
        return context

    def get_object(self, queryset=None):
        # Use a custom queryset if provided; this is required for subclasses
        # like DateDetailView
        if queryset is None:
            queryset = self.get_queryset()

        company_slug = self.kwargs.get('company_slug')
        balance_year = self.kwargs.get('balance_year')

        indicatorId = self.kwargs.get('indicator_id')
        indicatorStakeholder = indicatorId[:1]

        if indicatorId.startswith('n'): # negative indicator
            indicatorValue = indicatorId[1:]
            return queryset.get(
                company_balance__company__slug=company_slug,
                company_balance__year=balance_year,
                indicator__stakeholder=indicatorStakeholder,
                indicator__subindicator_number=indicatorValue,
                indicator__parent=None
            )

        else:
            indicatorValue = indicatorId[1:2]
            return queryset.get(
                company_balance__company__slug=company_slug,
                company_balance__year=balance_year,
                indicator__stakeholder=indicatorStakeholder,
                indicator__ecg_value=indicatorValue,
                indicator__parent=None
            )


class CompanyBalanceIndicatorCreateView(CreateView):
    model = CompanyBalanceIndicator


class CompanyBalanceIndicatorUpdateView(UpdateView):
    model = CompanyBalanceIndicator

    def get_success_url(self):
        return reverse('indicator-detail', kwargs={
            'company_slug': self.object.company_balance.company.slug,
            'balance_year': self.object.company_balance.year,
            'indicator_id': self.object.indicator
        })

    def form_valid(self, form):
        raise Exception, "here"

    def post(self, request, *args, **kwargs):
        companyBalanceIndicator = self.get_object()
        indicatorId = companyBalanceIndicator.indicator.slugify()

        post = self.request.POST
        indicatorPoints = int(post.get('indicator-points'))
        indicatorText = post.get('company-balance-indicator-%s-editor' % indicatorId)

        companyBalanceIndicator.evaluation = indicatorPoints
        companyBalanceIndicator.description = indicatorText
        companyBalanceIndicator.save()

        parent = companyBalanceIndicator.indicator.parent
        if parent:
            companyBalanceSubIndicators = CompanyBalanceIndicator.objects.filter(company_balance=companyBalanceIndicator.company_balance, indicator__parent=parent)

            subindicators_points_sum = 0
            for companyBalanceSubIndicator in companyBalanceSubIndicators:

                companyBalanceSubIndicatorPoints = 0
                if companyBalanceSubIndicator is companyBalanceIndicator:
                    companyBalanceSubIndicatorPoints = self.calculate_subindicator_points(indicatorPoints, companyBalanceIndicator, companyBalanceSubIndicators)
                else:
                    companyBalanceSubIndicatorPoints = self.calculate_subindicator_points(companyBalanceSubIndicator.evaluation, companyBalanceSubIndicator, companyBalanceSubIndicators)

                subindicators_points_sum += companyBalanceSubIndicatorPoints

            sum_percentage = round (( float(subindicators_points_sum) / parent.max_evaluation), 2) * 100
            rounded_sum_percentage = round(sum_percentage, -1)
            final_points = int ((rounded_sum_percentage * parent.max_evaluation) / 100)

            # set the company balance indicator points
            parentCBIndicator = CompanyBalanceIndicator.objects.get(company_balance=companyBalanceIndicator.company_balance, indicator=parent)
            parentCBIndicator.evaluation = final_points
            parentCBIndicator.save()

        self.object = companyBalanceIndicator

        return HttpResponseRedirect(self.get_success_url())
        #raise Exception, self.request.POST

    def calculate_subindicator_points(self, subindicatorPercentage, companyBalanceSubindicator, companyBalanceSubIndicators):

        """

        @param subindicatorPercentage: the subindicator percentage points
        @param companyBalanceSubindicator: the company balance sub indicator
        @param companyBalanceSubIndicators: all subindicators
        @return: @rtype: the calculated points for the subindicator
        """
        relevance_mapping = Indicator.RELEVANCE_MAPPING
        subindicator_relevance = relevance_mapping[companyBalanceSubindicator.indicator.relevance]
        subindicators_relevances_sum = 0

        # Subindicator Points = Prozent * Indicator MaxPoints * (high,3/middle,3/low,1,/no,0) / (3  + 2 + 1)

        # calculate the subindicator points
        for companyBalanceSubIndicator in companyBalanceSubIndicators:
            subindicators_relevances_sum += relevance_mapping[companyBalanceSubIndicator.indicator.relevance]

        parent = companyBalanceSubindicator.indicator.parent
        subindicator_area_points = parent.max_evaluation * (float (subindicator_relevance) / float(subindicators_relevances_sum) )
        subindicator_calculated_points = int (round ((float(subindicatorPercentage) / 100) * subindicator_area_points))

        return subindicator_calculated_points