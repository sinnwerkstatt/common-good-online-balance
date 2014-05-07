# -*- coding: utf-8 -*-
from crispy_forms.layout import Layout, HTML

from django import forms
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from ecg_balancing.models import UserProfile, Company


class UserProfileForm(forms.ModelForm):
    helper = FormHelper()
    helper.label_class = 'clearboth text-right col-lg-2 col-md-2'
    helper.field_class = 'col-lg-5 col-md-5'
    helper.form_tag = False

    class Meta:
        model = UserProfile
        #fields = ('user.first_name', 'user.last_name', 'user.email')
        #exclude = ['creation_date']


class CompanyForm(forms.ModelForm):
    helper = FormHelper()
    helper.label_class = 'clearboth text-right col-lg-2 col-md-2'
    helper.field_class = 'col-lg-5 col-md-5'
    helper.form_tag = False

    class Meta:
        model = Company
        #fields = ('user.first_name', 'user.last_name', 'user.email')
        exclude = ['model_creation_date']
