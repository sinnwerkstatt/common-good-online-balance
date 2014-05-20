# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext, Context
from django.template.loader import get_template

from django.views.generic import CreateView, DetailView, UpdateView, ListView, TemplateView, FormView
from ecg_balancing.forms import UserProfileForm, CompanyForm, CompanyBalanceForm, CompanyBalanceEditForm, FeedbackIndicatorForm

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

    def get_success_url(self):
        return reverse('user-detail', kwargs={'pk': self.request.user.pk})


class UserRoleMixin(object):
    """provides the variables 'has_company_access', 'is_admin' and 'is_guest' in the context. Requires the URL parameters 'company_slug' or 'slug' """

    def get_context_data(self, **kwargs):
        context = super(UserRoleMixin, self).get_context_data(**kwargs)

        if self.request.user.is_authenticated():
            company_slug = self.kwargs.get('company_slug')
            if company_slug is None:
                company_slug = self.kwargs.get('slug')

            company = Company.objects.get(slug=company_slug)

            try:
                userrole = UserRole.objects.get(user=self.request.user, company=company)
                context['has_company_access'] = True
                context['is_admin'] = (userrole.role == 'admin')
                context['is_guest'] = (userrole.role == 'guest')
            except:
                context['has_company_access'] = False
                context['company_name'] = company.name

        return context

    def render_to_response(self, context, **response_kwargs):
        has_company_access = context['has_company_access']
        if not has_company_access:
            return render_to_response('ecg_balancing/company_no_access.html',
                                      context,
                                      context_instance=RequestContext(self.request))

        else:
            return super(UserRoleMixin, self).render_to_response(context, **response_kwargs)


class CompanyDetailView(UserRoleMixin, DetailView):
    model = Company


class CompanyUpdateView(UserRoleMixin, UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = 'ecg_balancing/company_update.html'

    def get_success_url(self):
        if 'slug' in self.kwargs:
            slug = self.kwargs['slug']
            return reverse('company-detail', kwargs={'slug': slug})
        else:
            return super(CompanyUpdateView, self).get_success_url()


def getIndicatorStakeholder(indicatorId):
    return indicatorId[:1]

def getIndicatorValue(indicatorId):
    if indicatorId.startswith('n'): # negative indicator
        return indicatorId[1:]
    else:
        return indicatorId[1:2]


class CompanyBalanceDetailView(UserRoleMixin, DetailView):
    model = CompanyBalance
    template_name = 'ecg_balancing/company_balance_detail.html'

    def get_context_data(self, **kwargs):
        context = super(CompanyBalanceDetailView, self).get_context_data(**kwargs)
        context['indicators'] = self.object.company_balance.filter(indicator__parent=None).order_by('indicator__stakeholder')
        #raise Exception, self.request.user.role
        return context

    def get_object(self, queryset=None):
        # Use a custom queryset if provided; this is required for subclasses
        # like DateDetailView
        if queryset is None:
            queryset = self.get_queryset()

        return queryset.get(company__slug=self.kwargs.get('company_slug'), year=self.kwargs.get('balance_year'))



class CompanyBalanceCreateView(UserRoleMixin, CreateView):
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


class CompanyBalanceUpdateView(UserRoleMixin, UpdateView):
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


class CompanyBalanceIndicatorDetailView(UserRoleMixin, DetailView):
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
        indicatorStakeholder = getIndicatorStakeholder(indicatorId)
        indicatorValue = getIndicatorValue(indicatorId)

        if indicatorId.startswith('n'): # negative indicator
            return queryset.get(
                company_balance__company__slug=company_slug,
                company_balance__year=balance_year,
                indicator__stakeholder=indicatorStakeholder,
                indicator__subindicator_number=indicatorValue,
                indicator__parent=None
            )

        else:
            return queryset.get(
                company_balance__company__slug=company_slug,
                company_balance__year=balance_year,
                indicator__stakeholder=indicatorStakeholder,
                indicator__ecg_value=indicatorValue,
                indicator__parent=None
            )


class CompanyBalanceIndicatorCreateView(UserRoleMixin, CreateView):
    model = CompanyBalanceIndicator


# TODO: add UserRoleMixin for CompanyBalanceIndicatorUpdateView? URL needs 'company_slug' or 'slug'
class CompanyBalanceIndicatorUpdateView(UserRoleMixin, UpdateView):
    model = CompanyBalanceIndicator

    def get_success_url(self):

        # if subindicator is updated, redirect to the parent indicator URL
        indicator = self.object.indicator
        if indicator.parent:
            indicator = indicator.parent

        return reverse('indicator-detail', kwargs={
            'company_slug': self.object.company_balance.company.slug,
            'balance_year': self.object.company_balance.year,
            'indicator_id': indicator
        })

    def post(self, request, *args, **kwargs):
        companyBalanceIndicator = self.get_object()
        indicatorId = companyBalanceIndicator.indicator.slugify()

        post = self.request.POST
        indicatorText = post.get('company-balance-indicator-%s-editor' % indicatorId)
        if indicatorText:
            companyBalanceIndicator.description = indicatorText

        indicatorPointsPost = post.get('indicator-points')
        indicatorPoints = 0
        if indicatorPointsPost:
            indicatorPoints = int(indicatorPointsPost)
            companyBalanceIndicator.evaluation = indicatorPoints

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

        ## update Balance Points
        balance = companyBalanceIndicator.company_balance
        balance.points = self.calculate_balance_points(balance)
        balance.save()

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


    def calculate_balance_points(self, balance):

        """

        @param balance: the company balance
        @return: @rtype: the calculated balance points
        """
        calculated_points = 0
        balance_indicators = CompanyBalanceIndicator.objects.filter(company_balance=balance, indicator__parent=None)
        for balance_indicator in balance_indicators:
            balance_indicator_evaluation = balance_indicator.evaluation
            if balance_indicator_evaluation != 0:
                calculated_points += balance_indicator_evaluation

        return calculated_points


class FeedbackIndicatorFormView(FormView):
    form_class = FeedbackIndicatorForm
    template_name = 'ecg_balancing/feedback_indicator_form.html'
    indicator = None

    def get(self, request, *args, **kwargs):

        indicatorId = kwargs.get("indicator_id")
        indicatorStakeholder = getIndicatorStakeholder(indicatorId)
        indicatorValue = getIndicatorValue(indicatorId)

        if indicatorId.startswith('n'): # negative indicator
            self.indicator = Indicator.objects.get(stakeholder=indicatorStakeholder, subindicator_number=indicatorValue, parent=None)
        else:
            self.indicator = Indicator.objects.get(stakeholder=indicatorStakeholder, ecg_value=indicatorValue, parent=None)

        return super(FeedbackIndicatorFormView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(FeedbackIndicatorFormView, self).get_context_data(**kwargs)
        context.update({
            "indicator": self.indicator,
            "url": self.request.REQUEST['url'],
        })
        return context

    def get_initial(self, **kwargs):
        initial = super(FeedbackIndicatorFormView, self).get_initial()
        if self.request.method == "GET":
            initial.update({
                "indicator": self.indicator.pk,
            })

        return initial

    def form_valid(self, form):
        feedback_indicator = form.save()
        self.send_mail(feedback_indicator)
        return super(FeedbackIndicatorFormView, self).form_valid(form)

    def send_mail(self, feedback_indicator):
        # render attachment pdf
        plaintext = get_template('ecg_balancing/email/feedback_indicator_mail.txt')
        html = get_template('ecg_balancing/email/feedback_indicator_mail.html')
        context = Context({
            "sender_name": feedback_indicator.sender_name,
            "sender_email": feedback_indicator.sender_email,
            "message": feedback_indicator.message,
            "indicator": feedback_indicator.indicator,
        })
        text_content = plaintext.render(context)
        html_content = html.render(context)
        msg = EmailMultiAlternatives(
            _('[ECG] New Feedback for Indicator %s'%(str(feedback_indicator.indicator).upper())),
            text_content,
            settings.FEEDBACK_INDICATOR_SENDER_EMAIL,
            [feedback_indicator.indicator.contact],
            headers = {'Reply-To': feedback_indicator.sender_email})
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    def get_success_url(self):
        return reverse_lazy('feedback-indicator-success') + '?url=' + self.request.REQUEST['url']

class FeedbackIndicatorSuccessView(TemplateView):
    template_name = 'ecg_balancing/feedback_indicator_success.html'

