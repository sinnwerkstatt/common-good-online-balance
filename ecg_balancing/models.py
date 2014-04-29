# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime

from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.template.loader import get_template
from django.template.loader import render_to_string
from django.template import Context
from django.utils.translation import ugettext_lazy as _


# -------------------------------- MATRIX MODELS --------------------------------


MATRIX_VERSION_4_1 = '4.1'
MATRIX_VERSIONS = (
    (MATRIX_VERSION_4_1, MATRIX_VERSION_4_1),
)

STAKEHOLDERS = (
    'a', 'a',
    'b', 'b',
    'c', 'c',
    'd', 'd',
    'e', 'e',
)

ECG_VALUES = (
    '1', '1',
    '2', '2',
    '3', '3',
    '4', '4',
    '5', '5',
)


class ECGMatrix(models.Model):
    version = models.CharField(_('Version'), max_length=6, choices=MATRIX_VERSIONS,
                                      default=MATRIX_VERSION_4_1)
    contact = models.EmailField(_('Email'))

    class Meta:
        verbose_name = _('Matrix')
        verbose_name_plural = _('Matrices')

    def __unicode__(self):
        return self.version


class Indicator(models.Model):
    matrix = models.ForeignKey(ECGMatrix, verbose_name=_(u'Matrix'), related_name="matrix",
                              null=False,
                              blank=False)

    title = models.CharField(_('Name'), max_length=255)
    stakeholder = models.CharField(_('Stakeholder'), max_length=1, choices=STAKEHOLDERS)
    ecg_value = models.CharField(_('Value'), max_length=1, choices=ECG_VALUES)
    max_evaluation = models.CharField(_('Max Evaluation'), max_length=4)

    parent = models.ForeignKey(Indicator, verbose_name=_(u'Parent Indicator'), related_name="parent",
                              null=False,
                              blank=False)
    contact = models.EmailField(_('Email'))

    class Meta:
        verbose_name = _('Matrix')
        verbose_name_plural = _('Matrices')

    def __unicode__(self):
        return self.version


# -------------------------------- COMPANY MODELS --------------------------------


class Company(models.Model):
    name = models.CharField(_('Name'), max_length=255)
    logo = models.ImageField(_('Image'), blank=True, null=True, upload_to='company-upload')

    street = models.CharField(_('Street'), max_length=50, blank=False)
    zipcode = models.PositiveIntegerField(_('ZIP code'), blank=False)
    city = models.CharField(_('City'), max_length=50, blank=False)
    country = models.CharField(_('Country'), max_length=50, blank=False)
    website = models.CharField(_('Website'), blank=False)

    email = models.EmailField(_('Email'))
    phone = models.CharField(_('Phone Number'), blank=True, null=True)
    fax = models.CharField(_('Fax Number'), blank=True, null=True)

    # TODO: all 4 should be choices
    industry = models.CharField(_('Industry'), max_length=255, blank=True, null=True)
    activities = models.TextField(_('Activities'))
    employeesNumber = models.TextField(_('Number of employees'), blank=True, null=True)
    revenue = models.TextField(_('Revenue'), blank=True, null=True)

    foundation_date = models.DateTimeField(_('Foundation Date'), blank=True, null=True)
    owners = models.CharField(_('Owners'), max_length=255, blank=True, null=True)
    managing_directors = models.CharField(_('Managing Directors'), max_length=255, blank=True, null=True)

    # object creation date
    model_creation_date = models.DateTimeField(_('Model Creation Date'), default=datetime.datetime.now)

    class Meta:
        verbose_name = _('Company')
        verbose_name_plural = _('Companies')

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        path = reverse('company-detail', args=[self.pk])
        return path


class CompanyBalance(models.Model):
    matrix = models.ForeignKey(ECGMatrix, verbose_name=_(u'Matrix'), related_name="matrix",
                              null=False,
                              blank=False)

    start_date = models.DateTimeField(_('Start Date'), blank=True, null=True)
    end_date = models.DateTimeField(_('End Date'), blank=True, null=True)

    peer_companies = models.CharField(_('Peer Companies'), max_length=255, blank=True, null=True)
    auditor = models.CharField(_('Peer Companies'), max_length=255, blank=True, null=True)
    common_good = models.TextField(_('The Company and Common Good'), blank=True, null=True)
    prospect = models.TextField(_('Prospect'), blank=True, null=True)
    process_description = models.TextField(_('Balance process description'), blank=True, null=True)


    class Meta:
        verbose_name = _('Year Balance')
        verbose_name_plural = _('Year Balances')

    def __unicode__(self):
        return self.name

class CompanyBalanceIndicator(models.Model):
    company_balance = models.ForeignKey(CompanyBalance,
                            verbose_name=_(u'Company Balance'), related_name="company_balance",
                            null=False,
                            blank=False)
    indicator = models.ForeignKey(Indicator,
                            verbose_name=_(u'Indicator'), related_name="company_balance",
                            null=False,
                            blank=False)

    start_date = models.DateTimeField(_('Start Date'), blank=True, null=True)
    end_date = models.DateTimeField(_('End Date'), blank=True, null=True)

    description = models.CharField(_('Peer Companies'), max_length=255, blank=True, null=True)
    auditor = models.CharField(_('Peer Companies'), max_length=255, blank=True, null=True)
    common_good = models.TextField(_('The Company and Common Good'), blank=True, null=True)
    prospect = models.TextField(_('Prospect'), blank=True, null=True)
    process_description = models.TextField(_('Balance process description'), blank=True, null=True)


    class Meta:
        verbose_name = _('Year Balance')
        verbose_name_plural = _('Year Balances')

    def __unicode__(self):
        return self.name
