# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from ecg_balancing.models import UserProfile


class UserProfileForm(forms.ModelForm):
    helper = FormHelper()
    helper.label_class = 'clearboth pad-top-s textalignright col-lg-3 col-md-3'
    helper.field_class = 'pad-bottom col-lg-9 col-md-9'
    helper.form_tag = False

    class Meta:
        model = UserProfile
        #fields = ('user.first_name', 'user.last_name', 'user.email')
        #exclude = ['creation_date']

