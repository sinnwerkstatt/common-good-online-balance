# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Model
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from ecg_balancing.models import UserProfile, Company, Indicator, CompanyBalance, FeedbackIndicator, UserRole

from bootstrap3_datetime.widgets import DateTimePicker


class IndicatorForm(forms.ModelForm):
    class Meta:
        model = Indicator


class UserCreationForm2(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'duplicate_username': _("A user with that username already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }
    username = forms.RegexField(label=_("Username"), max_length=30,
        regex=r'^[\w.@+-]+$',
        help_text=_("Required. 30 characters or fewer. Letters, digits and "
                      "@/./+/-/_ only."),
        error_messages={
            'invalid': _("This value may contain only letters, numbers and "
                         "@/./+/-/_ characters.")})
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."))

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'])
        return password2


class UserAccountCreationForm(UserCreationForm2):
    error_messages_extended = {
        'duplicate_email': _("A user with that email already exists."),
    }

    first_name = forms.CharField(label=_(u'First Name'), max_length=30)
    last_name = forms.CharField(label=_(u'Last Name'), max_length=30)
    email = forms.CharField(label=_(u'Email'), max_length=255)

    helper = FormHelper()
    helper.label_class = 'clearboth text-right col-lg-2 col-md-2'
    helper.field_class = 'col-lg-5 col-md-5'
    helper.form_tag = False

    class Meta:
        model = UserProfile

    def __init__(self, *args, **kwargs):
        super(UserAccountCreationForm, self).__init__(*args, **kwargs)

        data = kwargs.get('data')
        if data:
            if data.get('username'):
                self.fields['username'].initial = data.get('username')
            if data.get('first_name'):
                self.fields['first_name'].initial = data.get('first_name')
            if data.get('last_name'):
                self.fields['last_name'].initial = data.get('last_name')
            if data.get('email'):
                self.fields['email'].initial = data.get('email')

        self.fields['password1'].required = True
        self.fields['password2'].required = True

        self.fields.keyOrder = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2',
        ]

    def clean_email(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        email = self.cleaned_data["email"]
        try:
            User._default_manager.get(email=email)
        except User.DoesNotExist:
            return email
        except:
            raise forms.ValidationError(self.error_messages_extended['duplicate_email'])
        raise forms.ValidationError(self.error_messages_extended['duplicate_email'])

    def save(self, commit=True, *args, **kwargs):

        # create user object
        username = self.data['username']
        email = self.data['email']
        first_name = self.data['first_name']
        last_name = self.data['last_name']
        password = self.data['password1']
        user = User.objects.create(
            username=username, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()

        # create userprofile object
        userprofile = super(UserAccountCreationForm, self).save(commit=False)
        userprofile.user = user
        if commit:
            userprofile.save()
        return userprofile


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(label=_(u'First Name'), max_length=30)
    last_name = forms.CharField(label=_(u'Last Name'), max_length=30)
    email = forms.CharField(label=_(u'Email'), max_length=255)

    helper = FormHelper()
    helper.label_class = 'clearboth text-right col-lg-2 col-md-2'
    helper.field_class = 'col-lg-5 col-md-5'
    helper.form_tag = False

    class Meta:
        model = UserProfile

    def __init__(self, user, *args, **kw):
        super(UserProfileForm, self).__init__(*args, **kw)
        self.user = user
        self.fields['first_name'].initial = self.instance.user.first_name
        self.fields['last_name'].initial = self.instance.user.last_name
        self.fields['email'].initial = self.instance.user.email
        self.fields.keyOrder = [
            'first_name',
            'last_name',
            'email',
            'avatar',
        ]

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            existing_user = User.objects.get(email=email)
            if existing_user.pk is not self.user.pk:
                raise forms.ValidationError(
                    _('A user with that email already exists.'))
        except User.DoesNotExist:
            return email
        except:
                raise forms.ValidationError(
                    _('A user with that email already exists.'))
        return email

    def save(self, *args, **kw):
        super(UserProfileForm, self).save(*args, **kw)
        self.instance.user.first_name = self.cleaned_data.get('first_name')
        self.instance.user.last_name = self.cleaned_data.get('last_name')
        self.instance.user.email = self.cleaned_data.get('email')
        self.instance.user.save()


class CompanyForm(forms.ModelForm):
    helper = FormHelper()
    helper.label_class = 'clearboth text-right col-lg-2 col-md-2'
    helper.field_class = 'col-lg-5 col-md-5'
    helper.form_tag = False
    
    foundation_date = forms.DateField(label=_("Foundation Date"),
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "viewMode": "years",
                                       "pickTime": False}))

    class Meta:
        model = Company
        #fields = ('user.first_name', 'user.last_name', 'user.email')
        exclude = ['model_creation_date', 'status']


class CompanyJoinForm(forms.ModelForm):

    class Meta:
        model = UserRole
        exclude = ['role', 'user']

    def __init__(self, user, *args, **kwargs):
        super(CompanyJoinForm, self ).__init__( *args, **kwargs )
        self.user = user

    def clean_company(self):
        company = self.cleaned_data['company']
        existing_role = UserRole.objects.filter(company=company, user=self.user)
        if existing_role.exists():
            raise forms.ValidationError(
                _('You already requested membership or you are member of this company.'))
        else:
            # company = Company.objects.get(pk=company)
            return company

    def save(self, *args, **kw):
        user = kw.pop('user')
        super(CompanyJoinForm, self).save(*args, **kw)
        company = self.instance.company

        user_role = UserRole.objects.create(company=company, user=user, role=UserRole.ROLE_CHOICE_PENDING)
        return user_role


class CompanyCreateForm(forms.ModelForm):

    class Meta:
        model = Company

    def __init__( self, user, *args, **kwargs ):
        super(CompanyCreateForm, self ).__init__( *args, **kwargs )
        self.user = user


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


class CompanyBalanceUpdateForm(forms.ModelForm):
    helper = FormHelper()
    helper.label_class = 'clearboth text-right col-lg-2 col-md-2'
    helper.field_class = 'col-lg-5 col-md-5'
    helper.form_tag = False

    start_date = forms.DateField(
        input_formats=['%Y-%m'], label=_("Start Date"),
        widget=DateTimePicker(options={"format": "YYYY-MM",
                                       "viewMode": "years",
                                       "pickTime": False}))

    end_date = forms.DateField(
        input_formats=['%Y-%m'], label=_("End Date"),
        widget=DateTimePicker(options={"format": "YYYY-MM",
                                       "viewMode": "years",
                                       "pickTime": False}))

    class Meta:
        model = CompanyBalance
        fields = ('matrix', 'year', 'start_date', 'end_date', 'status', 'visibility', 'evaluation_type', 'consultant', 'auditor', 'accompanying_consultant', 'peer_companies', 'employees_number', 'revenue', 'profit', 'worked_hours', 'number_participated_employees', 'common_good',
                  'process_description', 'internal_communication',
                  'prospect', 'company')

    def __init__(self, *args, **kwargs):
        super(CompanyBalanceUpdateForm, self).__init__(*args, **kwargs)
        self.fields['company'].widget = forms.HiddenInput()

        self.fields['status'].widget.attrs['disabled'] = 'disabled'
        self.fields['status'].required = False

        self.fields['visibility'].widget.attrs['disabled'] = 'disabled'
        self.fields['visibility'].required = False

    def clean_status(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.status
        else:
            return self.cleaned_data['status']

    def clean_visibility(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.visibility
        else:
            return self.cleaned_data['visibility']

    def clean(self):
        cleaned_data = super(CompanyBalanceUpdateForm, self).clean()
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
    sender_name = forms.CharField(widget=forms.HiddenInput())
    sender_email = forms.CharField(widget=forms.HiddenInput())

    helper = FormHelper()
    helper.label_class = 'clearboth text-right col-lg-2 col-md-2'
    helper.field_class = 'col-lg-5 col-md-5'
    helper.form_tag = False

    def __init__(self, user, *args, **kw):
        super(FeedbackIndicatorForm, self).__init__(*args, **kw)
        self.user = user

    class Meta:
        model = FeedbackIndicator
        exclude = ['receiver_name', 'receiver_email']

    def clean_indicator(self):
        data = self.cleaned_data['indicator']
        data = Indicator.objects.get(pk=data)
        return data