# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.core.validators import email_re, EMPTY_VALUES
from django.db.models import CharField
from django.utils.translation import ugettext_lazy as _

class CommaSeparatedEmailField(CharField):
    description = _('Email address(es)')

    def __init__(self, *args, **kwargs):
        self.token = kwargs.pop('token', ',')
        super(CommaSeparatedEmailField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        """
        Shows the list of emails as a string
        """
        if value in EMPTY_VALUES:
            return ''
        else:
            value = (self.token + ' ').join(value)

        return value

    def clean(self, value, model_instance):
        """
        Check that the field contains one or more 'comma-separated' emails
        and normalizes the data to a list of the email strings.
        """
        value = [item.strip() for item in value.split(self.token) if item.strip()]
        value = list(set(value))

        if value in EMPTY_VALUES and self.required:
            raise forms.ValidationError(_('This field is required.'))

        for email in value:
            if not email_re.match(email):
                raise forms.ValidationError(_(u"'%s' is not a valid "
                                              "e-mail address.") % email)
        return value

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules(
        [],
        [
            "^ecg_balancing\.fields\.CommaSeparatedEmailField",
        ])
except ImportError:
    pass
