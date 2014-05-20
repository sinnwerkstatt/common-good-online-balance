# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from ecg_balancing.models import UserProfile, Company, Indicator, CompanyBalance, FeedbackIndicator


class IndicatorForm(forms.ModelForm):
    class Meta:
        model = Indicator


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(label=_(u'First Name'), max_length=30)
    last_name = forms.CharField(label=_(u'Last Name'), max_length=30)

    helper = FormHelper()
    helper.label_class = 'clearboth text-right col-lg-2 col-md-2'
    helper.field_class = 'col-lg-5 col-md-5'
    helper.form_tag = False

    class Meta:
        model = UserProfile
        #fields = ('user.first_name', 'user.last_name', 'user.email')
        #exclude = ['creation_date']

    def __init__(self, *args, **kw):
        super(UserProfileForm, self).__init__(*args, **kw)
        self.fields['first_name'].initial = self.instance.first_name
        self.fields['last_name'].initial = self.instance.last_name
        self.fields.keyOrder = [
            'first_name',
            'last_name',
            'avatar',
            'companies',
        ]

    def save(self, *args, **kw):
        super(UserProfileForm, self).save(*args, **kw)
        self.instance.first_name = self.cleaned_data.get('first_name')
        self.instance.last_name = self.cleaned_data.get('last_name')
        #self.instance.profile.avatar.file = self.cleaned_data.get('avatar')
        self.instance.save()


class CompanyForm(forms.ModelForm):
    helper = FormHelper()
    helper.label_class = 'clearboth text-right col-lg-2 col-md-2'
    helper.field_class = 'col-lg-5 col-md-5'
    helper.form_tag = False

    class Meta:
        model = Company
        #fields = ('user.first_name', 'user.last_name', 'user.email')
        exclude = ['model_creation_date']


class CompanyBalanceForm(forms.ModelForm):
    helper = FormHelper()
    helper.label_class = 'clearboth text-right col-lg-2 col-md-2'
    helper.field_class = 'col-lg-5 col-md-5'
    helper.form_tag = False

    class Meta:
        model = CompanyBalance
        fields = ('matrix', 'year', 'company')

    def __init__(self, *args, **kwargs):
        super(CompanyBalanceForm, self).__init__(*args, **kwargs)
        self.fields['company'].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super(CompanyBalanceForm, self).clean()
        year = cleaned_data.get("year")
        company = cleaned_data.get("company")

        existing_balance = CompanyBalance.objects.filter(company=company, year=year)
        if existing_balance.exists():
            raise forms.ValidationError(
                _('There is an existing balance for the year %s. Please enter another year.' % year))

        return cleaned_data


class CompanyBalanceEditForm(forms.ModelForm):
    helper = FormHelper()
    helper.label_class = 'clearboth text-right col-lg-2 col-md-2'
    helper.field_class = 'col-lg-5 col-md-5'
    helper.form_tag = False

    class Meta:
        model = CompanyBalance
        fields = ('matrix', 'year', 'status', 'start_date', 'end_date', 'peer_companies', 'auditor', 'common_good',
                  'prospect', 'process_description', 'company')

    def __init__(self, *args, **kwargs):
        super(CompanyBalanceEditForm, self).__init__(*args, **kwargs)
        self.fields['company'].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super(CompanyBalanceEditForm, self).clean()
        year = cleaned_data.get("year")
        company = cleaned_data.get("company")

        if (self.instance.year != year):
            existing_balance = CompanyBalance.objects.filter(company=company, year=year)
            if existing_balance.exists():
                raise forms.ValidationError(
                    _('There is an existing balance for the year %s. Please enter another year.' % year))

        return cleaned_data


class FeedbackIndicatorForm(forms.ModelForm):
    indicator = forms.CharField(widget=forms.HiddenInput())

    helper = FormHelper()
    helper.label_class = 'clearboth text-right col-lg-2 col-md-2'
    helper.field_class = 'col-lg-5 col-md-5'
    helper.form_tag = False

    class Meta:
        model = FeedbackIndicator
        exclude = ['receiver_name', 'receiver_email']

    def clean_indicator(self):
        data = self.cleaned_data['indicator']
        data = Indicator.objects.get(pk=data)
        return data
