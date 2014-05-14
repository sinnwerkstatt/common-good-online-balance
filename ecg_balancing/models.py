# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime

from django.contrib.sites.models import Site
from django.contrib.auth.models import User, AbstractUser
from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.conf import settings
from django.db import models
from django.db.models import signals
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
    ('a', 'a'),
    ('b', 'b'),
    ('c', 'c'),
    ('d', 'd'),
    ('e', 'e'),
    ('n', 'n'),
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
    ECG_VALUE_1 = '1'
    ECG_VALUE_2 = '2'
    ECG_VALUE_3 = '3'
    ECG_VALUE_4 = '4'
    ECG_VALUE_5 = '5'
    ECG_VALUES = (
        (ECG_VALUE_1, _('Value 1')),
        (ECG_VALUE_2, _('Value 2')),
        (ECG_VALUE_3, _('Value 3')),
        (ECG_VALUE_4, _('Value 4')),
        (ECG_VALUE_5, _('Value 5')),
    )
    RELEVANCE_LOW = 'low'
    RELEVANCE_MIDDLE = 'middle'
    RELEVANCE_HIGH = 'high'
    RELEVANCE_VALUES = (
        (RELEVANCE_LOW, _('Low')),
        (RELEVANCE_MIDDLE, _('Middle')),
        (RELEVANCE_HIGH, _('High'))
    )
    RELEVANCE_MAPPING = {
        RELEVANCE_LOW: 1,
        RELEVANCE_MIDDLE: 2,
        RELEVANCE_HIGH: 3
    }

    matrix = models.ForeignKey('ecg_balancing.ECGMatrix', verbose_name=_(u'Matrix'), related_name='indicators',
                              null=False,
                              blank=False)

    title = models.CharField(_('Name'), max_length=255)
    stakeholder = models.CharField(_('Stakeholder'), max_length=1, choices=STAKEHOLDERS)
    ecg_value = models.CharField(_('Value'), max_length=1, choices=ECG_VALUES)
    max_evaluation = models.IntegerField(_('Max Evaluation'),
                                            help_text=_('Only for an indicator, without a parent.'),
                                            null=True,
                                            blank=True)

    parent = models.ForeignKey('ecg_balancing.Indicator', verbose_name=_(u'Parent Indicator'), related_name='parent_indicator',
                              null=True,
                              blank=True)
    subindicator_number = models.IntegerField(_('Subindicator Number'),
                                                help_text=_('Only for a subindicator, an indicator with a parent.'),
                                                null=True,
                                                blank=True)
    relevance = models.CharField(_('Relevance'), max_length=10, choices=RELEVANCE_VALUES,
                                        help_text=_('Only for a subindicator, an indicator with a parent.'),
                                                null=True,
                                                blank=True)

    editor = models.CharField(_('Editor'),  max_length=30, blank=True, null=True)
    contact = models.EmailField(_('Email'), blank=True, null=True)

    class Meta:
        verbose_name = _('Indicator')
        verbose_name_plural = _('Indicators')

    def __unicode__(self):
        if self.stakeholder.startswith('n'):
            return '%s%s' % (
                unicode(self.stakeholder),
                unicode(self.subindicator_number)
            )
        elif self.parent is None:
            return '%s%s' % (
                unicode(self.stakeholder),
                unicode(self.ecg_value)
            )
        else:
            return '%s%s.%s' % (
                unicode(self.stakeholder),
                unicode(self.ecg_value),
                unicode(self.subindicator_number)
            )

    def slugify(self):
        if self.stakeholder.startswith('n'):
            return '%s%s' % (
                unicode(self.stakeholder),
                unicode(self.subindicator_number)
            )
        elif self.parent is None:
            return '%s%s' % (
                unicode(self.stakeholder),
                unicode(self.ecg_value)
            )
        else:
            return '%s%s-%s' % (
                unicode(self.stakeholder),
                unicode(self.ecg_value),
                unicode(self.subindicator_number)
            )



# -------------------------------- COMPANY MODELS --------------------------------


class Company(models.Model):
    INDUSTRY_CHOICE_AEROSPACE_AND_DEFENSE = 'aerospace_and_defense'
    INDUSTRY_CHOICE_AUTO = 'auto'
    INDUSTRY_CHOICE_BANKS_AND_FINANCIAL = 'banks_and_financial'
    INDUSTRY_CHOICE_BIOTECH_AND_CHEMICALS = 'biotech_and_chemicals'
    INDUSTRY_CHOICE_COMPUTERS_AND_HARDWARE = 'computers_and_hardware'
    INDUSTRY_CHOICE_CONSULTING_AND_BUSINESS_SERVICES = 'consulting_and_business_services'
    INDUSTRY_CHOICE_EDUCATION_AND_SCHOOLS = 'education_and_schools'
    INDUSTRY_CHOICE_ENERGY_AND_UTILITIES = 'energy_and_utilities'
    INDUSTRY_CHOICE_ENGINEERING_AND_CONSTRUCTION = 'engineering_and_construction'
    INDUSTRY_CHOICE_FARMING_AND_AGRICULTURE = 'farming_and_agriculture'
    INDUSTRY_CHOICE_FASHION_AND_BEAUTY = 'fashion_and_beauty'
    INDUSTRY_CHOICE_FOOD_AND_BEVERAGES = 'food_and_beverages'
    INDUSTRY_CHOICE_GOVERNMENTAL_ORGANIZATION = 'governmental_organization'
    INDUSTRY_CHOICE_HEALTH = 'health'
    INDUSTRY_CHOICE_INDUSTRIALS = 'industrials'
    INDUSTRY_CHOICE_INSURANCE = 'insurance'
    INDUSTRY_CHOICE_INTERNET_AND_SOFTWARE = 'internet_and_software'
    INDUSTRY_CHOICE_LEGAL = 'legal'
    INDUSTRY_CHOICE_MEDIA_NEWS_AND_PUBLISHING = 'media_news_and_publishing'
    INDUSTRY_CHOICE_MINING_AND_MATERIALS = 'mining_and_materials'
    INDUSTRY_CHOICE_NON_PROFIT = 'non_profit'
    INDUSTRY_CHOICE_POLITICAL_ORGANIZATION = 'political_organization'
    INDUSTRY_CHOICE_PROFESSIONAL_SERVICES = 'professional_services'
    INDUSTRY_CHOICE_RELIGIOUS_ORGANIZATION = 'religious_organization'
    INDUSTRY_CHOICE_RETAIL_AND_CONSUMER_MERCHANDISE = 'retail_and_consumer_merchandise'
    INDUSTRY_CHOICE_TELECOMMUNICATIONS = 'telecommunications'
    INDUSTRY_CHOICE_TRANSPORT_AND_FREIGHT = 'transport_and_freight'
    INDUSTRY_CHOICE_TRAVEL_AND_LEISURE = 'travel_and_leisure'
    INDUSTRY_CHOICE_COMPANY = 'company'
    INDUSTRY_CHOICE_INSTITUTION = 'institution'
    INDUSTRY_CHOICE_ORGANIZATION = 'organization'
    INDUSTRY_CHOICE_OTHER = 'other'
    INDUSTRY_CHOICES = (
        (INDUSTRY_CHOICE_AEROSPACE_AND_DEFENSE, _('Aerospace and Defense')),
        (INDUSTRY_CHOICE_AUTO, _('Auto')),
        (INDUSTRY_CHOICE_BANKS_AND_FINANCIAL, _('Banks and Financial')),
        (INDUSTRY_CHOICE_BIOTECH_AND_CHEMICALS, _('Biotech and Chemicals')),
        (INDUSTRY_CHOICE_COMPUTERS_AND_HARDWARE, _('Computers and Hardware')),
        (INDUSTRY_CHOICE_CONSULTING_AND_BUSINESS_SERVICES, _('Consulting and Business Services')),
        (INDUSTRY_CHOICE_EDUCATION_AND_SCHOOLS, _('Education and Schools')),
        (INDUSTRY_CHOICE_ENERGY_AND_UTILITIES, _('Energy and Utilities')),
        (INDUSTRY_CHOICE_ENGINEERING_AND_CONSTRUCTION, _('Engineering and Construction')),
        (INDUSTRY_CHOICE_FARMING_AND_AGRICULTURE, _('Farming and Agriculture')),
        (INDUSTRY_CHOICE_FASHION_AND_BEAUTY, _('Fashion and Beauty')),
        (INDUSTRY_CHOICE_FOOD_AND_BEVERAGES, _('Food and Beverages')),
        (INDUSTRY_CHOICE_GOVERNMENTAL_ORGANIZATION, _('Governmental Organization')),
        (INDUSTRY_CHOICE_HEALTH, _('Health')),
        (INDUSTRY_CHOICE_INDUSTRIALS, _('Industrials')),
        (INDUSTRY_CHOICE_INSURANCE, _('Insurance')),
        (INDUSTRY_CHOICE_INTERNET_AND_SOFTWARE, _('Internet and Software')),
        (INDUSTRY_CHOICE_LEGAL, _('Legal')),
        (INDUSTRY_CHOICE_MEDIA_NEWS_AND_PUBLISHING, _('Media, News and Publishing')),
        (INDUSTRY_CHOICE_MINING_AND_MATERIALS, _('Mining and Materials')),
        (INDUSTRY_CHOICE_NON_PROFIT, _('Non-profit')),
        (INDUSTRY_CHOICE_POLITICAL_ORGANIZATION, _('Political Organization')),
        (INDUSTRY_CHOICE_PROFESSIONAL_SERVICES, _('Professional Services')),
        (INDUSTRY_CHOICE_RELIGIOUS_ORGANIZATION, _('Religious Organization')),
        (INDUSTRY_CHOICE_RETAIL_AND_CONSUMER_MERCHANDISE, _('Retail and Consumer Merchandise')),
        (INDUSTRY_CHOICE_TELECOMMUNICATIONS, _('Telecommunications')),
        (INDUSTRY_CHOICE_TRANSPORT_AND_FREIGHT, _('Transport and Freight')),
        (INDUSTRY_CHOICE_TRAVEL_AND_LEISURE, _('Travel and Leisure')),
        (INDUSTRY_CHOICE_COMPANY, _('Company')),
        (INDUSTRY_CHOICE_INSTITUTION, _('Institution')),
        (INDUSTRY_CHOICE_ORGANIZATION, _('Organization')),
        (INDUSTRY_CHOICE_OTHER, _('Other'))
    )
    ACTIVITY_CHOICE_EXAMPLE = 'example'
    ACTIVITY_CHOICES = (
        (ACTIVITY_CHOICE_EXAMPLE, _('Example')),
    )
    EMPLOYEES_NUMBER_CHOICE_ONE = 'one'
    EMPLOYEES_NUMBER_CHOICE_SMALL = 'small'
    EMPLOYEES_NUMBER_CHOICE_MEDIUM = 'medium'
    EMPLOYEES_NUMBER_CHOICE_LARGE = 'large'
    EMPLOYEES_NUMBER_CHOICES = (
        (EMPLOYEES_NUMBER_CHOICE_ONE, _('1 employee')),
        (EMPLOYEES_NUMBER_CHOICE_SMALL, _('1-10 employees')),
        (EMPLOYEES_NUMBER_CHOICE_MEDIUM, _('11-50 employees')),
        (EMPLOYEES_NUMBER_CHOICE_LARGE, _('More than 50 employees'))
    )
    REVENUE_CHOICE_SMALL = 'small'
    REVENUE_CHOICE_MEDIUM = 'medium'
    REVENUE_CHOICE_LARGE = 'large'
    REVENUE_CHOICES = (
        (REVENUE_CHOICE_SMALL, _('0 - 100.000 USD')),
        (REVENUE_CHOICE_MEDIUM, _('100.000 - 500.000 USD')),
        (REVENUE_CHOICE_LARGE, _('More than 500.000 USD'))
    )

    name = models.CharField(_('Name'), max_length=255)
    slug = models.SlugField(_('Slug'), max_length=50, unique=True)
    logo = models.ImageField(_('Image'), blank=True, null=True, upload_to='company-upload')

    street = models.CharField(_('Street'), max_length=50, blank=False)
    zipcode = models.PositiveIntegerField(_('ZIP code'), blank=False)
    city = models.CharField(_('City'), max_length=50, blank=False)
    country = models.CharField(_('Country'), max_length=50, blank=False)
    website = models.CharField(_('Website'), max_length=255, blank=False)

    email = models.EmailField(_('Email'))
    phone = models.CharField(_('Phone Number'), max_length=50, blank=True, null=True)
    fax = models.CharField(_('Fax Number'), max_length=50, blank=True, null=True)

    # TODO: all 4 should be choices
    industry = models.CharField(_('Industry'), max_length=255, choices=INDUSTRY_CHOICES, blank=True, null=True)
    activities = models.CharField(_('Activities'), max_length=255, choices=ACTIVITY_CHOICES, blank=True, null=True)
    employees_number = models.CharField(_('Number of employees'), max_length=255, choices=EMPLOYEES_NUMBER_CHOICES)
    revenue = models.CharField(_('Revenue'), max_length=255, choices=REVENUE_CHOICES, blank=True, null=True)

    foundation_date = models.DateTimeField(_('Foundation Date'), blank=True, null=True)
    owners = models.CharField(_('Owners'), max_length=255, blank=True, null=True)
    managing_directors = models.CharField(_('Managing Directors'), max_length=255, blank=True, null=True)

    # object creation date
    model_creation_date = models.DateTimeField(_('Model Creation Date'), default=datetime.datetime.now)

    class Meta:
        verbose_name = _('Company')
        verbose_name_plural = _('Companies')

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        path = reverse('company-detail', args=[self.pk])
        return path


class CompanyBalance(models.Model):
    matrix = models.ForeignKey('ecg_balancing.ECGMatrix', verbose_name=_(u'Matrix'), related_name='company_balances',
                              null=False,
                              blank=False)
    company = models.ForeignKey('ecg_balancing.Company', verbose_name=_(u'Company'), related_name='balance',
                              null=False,
                              blank=False)
    STATUS_CHOICE_STARTED = 'started'
    STATUS_CHOICE_FINISHED = 'finished'
    STATUS_CHOICE_AUDITED = 'audited'
    STATUS_CHOICE = (
        (STATUS_CHOICE_STARTED, _('Started')),
        (STATUS_CHOICE_FINISHED, _('Finished')),
        (STATUS_CHOICE_AUDITED, _('Audited'))
    )
    status = models.CharField(_('Status'), max_length=255, choices=STATUS_CHOICE, null=False, blank=False)

    year = models.SmallIntegerField(_('Year'), max_length=4)
    start_date = models.DateTimeField(_('Start Date'), blank=True, null=True)
    end_date = models.DateTimeField(_('End Date'), blank=True, null=True)

    peer_companies = models.ManyToManyField('ecg_balancing.Company', verbose_name=_('Peer Companies'), max_length=255, blank=True, null=True)
    auditor = models.CharField(_('Auditor'), max_length=255, blank=True, null=True)
    common_good = models.TextField(_('The Company and Common Good'), blank=True, null=True)
    prospect = models.TextField(_('Prospect'), blank=True, null=True)
    process_description = models.TextField(_('Balance process description'), blank=True, null=True)


    class Meta:
        verbose_name = _('Year Balance')
        verbose_name_plural = _('Year Balances')

    def __unicode__(self):
        return '%s:%s:%s' % (
            unicode(self.company),
            unicode(self.matrix),
            unicode(self.year)
        )


def create_company_balance(**kwargs):
    created = kwargs.get('created')

    # create indicators only when the balance is created, not when it is saved
    if created:
        balance = kwargs.get('instance')

        # create company balance indicators
        company_balance_indicators = []

        indicators = Indicator.objects.all()
        for indicator in indicators:
            company_balance_indicators.append(CompanyBalanceIndicator(company_balance=balance, indicator=indicator))

        CompanyBalanceIndicator.objects.bulk_create(company_balance_indicators)


#def delete_company_balance(**kwargs):
#    balance = kwargs.get('instance')
#    print balance


signals.post_save.connect(create_company_balance, sender=CompanyBalance)
#signals.post_delete.connect(delete_company_balance, sender=CompanyBalance)


class CompanyBalanceIndicator(models.Model):
    company_balance = models.ForeignKey('ecg_balancing.CompanyBalance',
                            verbose_name=_(u'Company Balance'), related_name='company_balance',
                            null=False,
                            blank=False)
    indicator = models.ForeignKey('ecg_balancing.Indicator',
                            verbose_name=_(u'Indicator'), related_name='company_balance',
                            null=False,
                            blank=False)

    description = models.TextField(_('Description'), blank=True, null=True)
    evaluation = models.IntegerField(_('Evaluation'), default=0)

    class Meta:
        verbose_name = _('Company Balance Indicator')
        verbose_name_plural = _('Company Balance Indicators')

    def __unicode__(self):
        return "%s: %s" % (
            unicode(self.company_balance),
            unicode(self.indicator)
        )


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, editable=False, related_name='profile')

    avatar = models.ImageField(_('Image'), blank=True, null=True, upload_to='profiles-upload')
    companies = models.ManyToManyField('ecg_balancing.Company', verbose_name=_('Companies'), blank=True, null=True)


class UserRole(models.Model):
    ROLE_CHOICE_ADMIN = 'admin'
    ROLE_CHOICE_GUEST = 'guest'
    ROLE_CHOICES = (
        (ROLE_CHOICE_ADMIN, _('Admin')),
        (ROLE_CHOICE_GUEST, _('Guest')),
    )

    company = models.ForeignKey('ecg_balancing.Company', verbose_name=_('Company'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('User'))
    role = models.CharField(_('Role'), max_length=5, choices=ROLE_CHOICES)

    class Meta:
        verbose_name = _('User Role')
        verbose_name_plural = _('User Roles')

    def __unicode__(self):
        return "%s: %s" % (
            unicode(self.company),
            unicode(self.user)
        )
