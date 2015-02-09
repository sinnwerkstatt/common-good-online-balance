# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime

from django.core.urlresolvers import reverse
from django.conf import settings
from django.db import models
from django.db.models import signals
from django.utils.translation import ugettext_lazy as _
from osm_field.fields import OSMField

from ecg_balancing import fields


# -------------------------------- MATRIX MODELS --------------------------------
from ecg_balancing.managers import CompanyBalanceIndicatorManager, CompanyManager

MATRIX_VERSION_4_1 = '4.1'
MATRIX_VERSIONS = (
    (MATRIX_VERSION_4_1, MATRIX_VERSION_4_1),
)

STAKEHOLDERS = (
    ('a', _('Suppliers')),
    ('b', _('Investors')),
    ('c', _('Employees, including business owners')),
    ('d', _('Customers, Products, Services, Business Partners')),
    ('e', _('Social Environment: Region, electorate, future generations, civil society, fellow human beings, animals and plants')),
    ('n', _('Negative Criteria')),
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
        (ECG_VALUE_1, _('Human Dignity')),
        (ECG_VALUE_2, _('Cooperation and Solidarity')),
        (ECG_VALUE_3, _('Ecological Sustainability')),
        (ECG_VALUE_4, _('Social Justice')),
        (ECG_VALUE_5, _('Democratic Co-determination and Transparency')),
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
    relevance = models.CharField(_('Relevance'), max_length=10, choices=RELEVANCE_VALUES, default=RELEVANCE_MIDDLE, 
                                        help_text=_('Only for a subindicator, an indicator with a parent.'),
                                                null=True,
                                                blank=True)
    sole_proprietorship = models.BooleanField(_('Applicable for sole proprietorship?'), default=True)


    editor = models.CharField(_('Editor'),  max_length=30, blank=True, null=True)
    contact = fields.CommaSeparatedEmailField(_('Email(s)'),
                                              help_text=_('Multiple emails should be separated with a comma'),
                                              max_length=255, blank=True, null=True)

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

    INDUSTRY_CHOICE_CONSTRUCTION = 'construction'
    INDUSTRY_CHOICE_MINING_AND_QUARRYING = 'mining_and_quarrying'
    INDUSTRY_CHOICE_PROFESSIONAL_SCIENTIFIC_AND_TECHNICAL_SERVICE_ACTIVITIES = 'professional_scientific_and_technical_service_activities'
    INDUSTRY_CHOICE_OTHER_SERVICE_ACTIVITIES = 'other_service_activities'
    INDUSTRY_CHOICE_ADMINISTRATIVE_AND_SUPPORT_SERVICE_ACTIVITIES = 'administrative_and_support_service_activities'
    INDUSTRY_CHOICE_ELECTRICITY_GAS_STEAM_AND_AIR_CONDITIONING_SUPPLY = 'electricity_gas_steam_and_air_conditioning_supply'
    INDUSTRY_CHOICE_EDUCATION = 'education'
    INDUSTRY_CHOICE_ACTIVITIES_OF_EXTRATERRITORIAL_ORGANISATIONS_AND_BODIES = 'activities_of_extraterritorial_organisations_and_bodies'
    INDUSTRY_CHOICE_FINANCIAL_AND_INSURANCE_ACTIVITIES = 'financial_and_insurance_activities'
    INDUSTRY_CHOICE_RESEARCH_AND_DEVELOPMENT = 'research_and_development'
    INDUSTRY_CHOICE_GARDENERS_AND_FLORISTS = 'gardeners_and_florists'
    INDUSTRY_CHOICE_HUMAN_HEALTH_AND_SOCIAL_WORK_ACTIVITIES = 'human_health_and_social_work_activities'
    INDUSTRY_CHOICE_WHOLESALE_AND_RETAIL_TRADE_REPAIR_OF_MOTOR_VEHICLES_AND_MOTORCYCLES = 'wholesale_and_retail_trade_repair_of_motor_vehicles_and_motorcycles'
    INDUSTRY_CHOICE_REAL_ESTATE_ACTIVITIES = 'real_estate_activities'
    INDUSTRY_CHOICE_OTHER_INDUSTRIES = 'other_industries'
    INDUSTRY_CHOICE_CHARITABLE_ORGANIZATIONS_NGO = 'charitable_organizations_ngo'
    INDUSTRY_CHOICE_CHURCH_AND_RELIGIOUS_INSTITUTIONS = 'church_and_religious_institutions'
    INDUSTRY_CHOICE_ART_AND_CULTURE = 'art_and_culture'
    INDUSTRY_CHOICE_AGRICULTURE_FORESTRY_AND_FISHING = 'agriculture_forestry_and_fishing'
    INDUSTRY_CHOICE_FOOD_INDUSTRIES = 'food_industries'
    INDUSTRY_CHOICE_MEDIA_MANAGEMENT_ADVERTISING_AND_MARKET_COMMUNICATION = 'media_management_advertising_and_market_communication'
    INDUSTRY_CHOICE_METAL_AND_ELECTRICAL_INDUSTRY = 'metal_and_electrical_industry'
    INDUSTRY_CHOICE_PUBLIC_ADMINISTRATION_AND_DEFENCE_COMPULSORY_SOCIAL_SECURITY = 'public_administration_and_defence_compulsory_social_security'
    INDUSTRY_CHOICE_POLITICS_POLITICAL_ACTIONS = 'politics_political_actions'
    INDUSTRY_CHOICE_ACTIVITIES_OF_HOUSEHOLDS_AS_EMPLOYERS = 'activities_of_households_as_employers'
    INDUSTRY_CHOICE_LAW_LAWYER_TAX_CONSULTANCY = 'law_lawyer_tax_consultancy'
    INDUSTRY_CHOICE_TEXTILES_CLOTHING_SHOE_AND_LEATHER_INDUSTRY = 'textiles_clothing_shoe_and_leather_industry'
    INDUSTRY_CHOICE_ACCOMMODATION_AND_FOOD_SERVICE_ACTIVITIES = 'accommodation_and_food_service_activities'
    INDUSTRY_CHOICE_TRANSPORTATION_AND_STORAGE = 'transportation_and_storage'
    INDUSTRY_CHOICE_CONSULTING_AND_IT_INDUSTRY = 'consulting_and_it_industry'
    INDUSTRY_CHOICE_MANUFACTURING = 'manufacturing'
    INDUSTRY_CHOICE_WATER_SUPPLY_SEWERAGE_WASTE_MANAGEMENT_AND_REMEDIATION_ACTIVITIES = 'water_supply_sewerage_waste_management_and_remediation_activities'
    
    INDUSTRY_CHOICES = (
        (INDUSTRY_CHOICE_CONSTRUCTION, _('Construction')),
        (INDUSTRY_CHOICE_MINING_AND_QUARRYING, _('Mining and quarrying')),
        (INDUSTRY_CHOICE_PROFESSIONAL_SCIENTIFIC_AND_TECHNICAL_SERVICE_ACTIVITIES, _('Professional, scientific and technical service activities')),
        (INDUSTRY_CHOICE_OTHER_SERVICE_ACTIVITIES, _('Other service activities')),
        (INDUSTRY_CHOICE_ADMINISTRATIVE_AND_SUPPORT_SERVICE_ACTIVITIES, _('Administrative and support service activities')),
        (INDUSTRY_CHOICE_ELECTRICITY_GAS_STEAM_AND_AIR_CONDITIONING_SUPPLY, _('Electricity, gas, steam and air conditioning supply')),
        (INDUSTRY_CHOICE_EDUCATION, _('Education')),
        (INDUSTRY_CHOICE_ACTIVITIES_OF_EXTRATERRITORIAL_ORGANISATIONS_AND_BODIES, _('Activities of extraterritorial organisations and bodies')),
        (INDUSTRY_CHOICE_FINANCIAL_AND_INSURANCE_ACTIVITIES, _('Financial and insurance activities')),
        (INDUSTRY_CHOICE_RESEARCH_AND_DEVELOPMENT, _('Research and development')),
        (INDUSTRY_CHOICE_GARDENERS_AND_FLORISTS, _('Gardeners and florists')),
        (INDUSTRY_CHOICE_HUMAN_HEALTH_AND_SOCIAL_WORK_ACTIVITIES, _('Human health and social work activities')),
        (INDUSTRY_CHOICE_WHOLESALE_AND_RETAIL_TRADE_REPAIR_OF_MOTOR_VEHICLES_AND_MOTORCYCLES, _('Wholesale and retail trade, repair of motor vehicles and motorcycles')),
        (INDUSTRY_CHOICE_REAL_ESTATE_ACTIVITIES, _('Real estate activities')),
        (INDUSTRY_CHOICE_OTHER_INDUSTRIES, _('Other industries')),
        (INDUSTRY_CHOICE_CHARITABLE_ORGANIZATIONS_NGO, _('Charitable organizations, NGOs')),
        (INDUSTRY_CHOICE_CHURCH_AND_RELIGIOUS_INSTITUTIONS, _('Church and religious institutions')),
        (INDUSTRY_CHOICE_ART_AND_CULTURE, _('Art and culture')),
        (INDUSTRY_CHOICE_AGRICULTURE_FORESTRY_AND_FISHING, _('Agriculture, forestry and fishing')),
        (INDUSTRY_CHOICE_FOOD_INDUSTRIES, _('Food industries')),
        (INDUSTRY_CHOICE_MEDIA_MANAGEMENT_ADVERTISING_AND_MARKET_COMMUNICATION, _('Media management, advertising and market communication')),
        (INDUSTRY_CHOICE_METAL_AND_ELECTRICAL_INDUSTRY, _('Metal and electrical industry')),
        (INDUSTRY_CHOICE_PUBLIC_ADMINISTRATION_AND_DEFENCE_COMPULSORY_SOCIAL_SECURITY, _('Public administration and defence, compulsory, social security')),
        (INDUSTRY_CHOICE_POLITICS_POLITICAL_ACTIONS, _('Politics, political actions')),
        (INDUSTRY_CHOICE_ACTIVITIES_OF_HOUSEHOLDS_AS_EMPLOYERS, _('Activities of households as employers')),
        (INDUSTRY_CHOICE_LAW_LAWYER_TAX_CONSULTANCY, _('Law (lawyer, tax consultancy, ...)')),
        (INDUSTRY_CHOICE_TEXTILES_CLOTHING_SHOE_AND_LEATHER_INDUSTRY, _('Textiles, clothing, shoe and leather industry')),
        (INDUSTRY_CHOICE_ACCOMMODATION_AND_FOOD_SERVICE_ACTIVITIES, _('Accommodation and food service activities')),
        (INDUSTRY_CHOICE_TRANSPORTATION_AND_STORAGE, _('Transportation and storage')),
        (INDUSTRY_CHOICE_CONSULTING_AND_IT_INDUSTRY, _('Consulting and IT industry')),
        (INDUSTRY_CHOICE_MANUFACTURING, _('Manufacturing')),
        (INDUSTRY_CHOICE_WATER_SUPPLY_SEWERAGE_WASTE_MANAGEMENT_AND_REMEDIATION_ACTIVITIES, _('Water supply, sewerage waste management and remediation activities')),
    )

    ACTIVITY_CHOICE_EXAMPLE = 'example'
    ACTIVITY_CHOICES = (
        (ACTIVITY_CHOICE_EXAMPLE, _('Example')),
    )

    VISIBILITY_CHOICE_BASIC = 'basic'
    VISIBILITY_CHOICE_ALL = 'all'
    VISIBILITY_CHOICES = (
        (VISIBILITY_CHOICE_BASIC, _('Logo, Name, Website')),
        (VISIBILITY_CHOICE_ALL, _('Everything')),
    )

    name = models.CharField(_('Name'), max_length=255)
    slug = models.SlugField(_('Slug'), max_length=50, unique=True)
    logo = models.ImageField(_('Image'), blank=True, null=True, upload_to='company-upload')

    street = models.CharField(_('Street'), max_length=50, blank=False)
    zipcode = models.PositiveIntegerField(_('ZIP code'), blank=False)
    city = models.CharField(_('City'), max_length=50, blank=False)
    country = models.CharField(_('Country'), max_length=50, blank=False)
    location = OSMField(_('Location'), blank=True, null=True)
    website = models.CharField(_('Website'), max_length=255, blank=False)

    email = models.EmailField(_('Email'), unique=True)
    phone = models.CharField(_('Phone Number'), max_length=50, blank=True, null=True)
    fax = models.CharField(_('Fax Number'), max_length=50, blank=True, null=True)

    industry = models.CharField(_('Industry'), max_length=255, choices=INDUSTRY_CHOICES, blank=True, null=True)
    activities = models.CharField(_('Activities'), max_length=255, blank=True, null=True)
    affiliates = models.CharField(_('Affiliates'), max_length=255, blank=True, null=True)

    foundation_date = models.DateField(_('Foundation Date'), blank=True, null=True)
    owners = models.CharField(_('Owners'), max_length=255, blank=True, null=True)
    managing_directors = models.CharField(_('Managing Directors'), max_length=255, blank=True, null=True)

    visibility = models.CharField(_('Visibility'), max_length=10, choices=VISIBILITY_CHOICES, default=VISIBILITY_CHOICE_BASIC)

    STATUS_CHOICE_NOT_APPROVED = 'not-approved'
    STATUS_CHOICE_APPROVED = 'approved'
    STATUS_CHOICES = (
        (STATUS_CHOICE_NOT_APPROVED, _('Not approved')),
        (STATUS_CHOICE_APPROVED, _('Approved')),
    )
    status = models.CharField(_('Status'), max_length=20, choices=STATUS_CHOICES, default=STATUS_CHOICE_NOT_APPROVED)

    # object creation date
    model_creation_date = models.DateTimeField(_('Model Creation Date'), default=datetime.datetime.now)

    objects = CompanyManager()

    class Meta:
        verbose_name = _('Company')
        verbose_name_plural = _('Companies')

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        path = reverse('company-detail', args=[self.pk])
        return path


class CompanyBalance(models.Model):
    company = models.ForeignKey('ecg_balancing.Company', verbose_name=_(u'Company'), related_name='balance',
                              null=False,
                              blank=False)

    points = models.SmallIntegerField(_('Points'), max_length=4, default=0)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Created by'), related_name='created_by', blank=True, null=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Updated by'), related_name='updated_by', blank=True, null=True)

    matrix = models.ForeignKey('ecg_balancing.ECGMatrix', verbose_name=_(u'Matrix'), related_name='company_balances',
                              null=False,
                              blank=False)

    year = models.SmallIntegerField(_('Year'), max_length=4)
    start_date = models.DateField(_('Start Date'), blank=True, null=True)
    end_date = models.DateField(_('End Date'), blank=True, null=True)

    STATUS_CHOICE_DRAFT = 'draft'
    STATUS_CHOICE_FINISHED = 'finished'
    STATUS_CHOICE_CERTIFIED = 'certified'
    STATUS_CHOICE_PUBLISHED = 'published'
    STATUS_CHOICE = (
        (STATUS_CHOICE_DRAFT, _('Draft')),
        (STATUS_CHOICE_FINISHED, _('Final / Finished')),
        (STATUS_CHOICE_CERTIFIED, _('Certified / Not published')),
        (STATUS_CHOICE_PUBLISHED, _('Published'))
    )
    status = models.CharField(_('Status'), max_length=255, choices=STATUS_CHOICE, null=False, blank=False)

    VISIBILITY_CHOICE_INTERNAL = 'internal'
    VISIBILITY_CHOICE_PUBLIC = 'public'
    VISIBILITY_CHOICE = (
        (VISIBILITY_CHOICE_INTERNAL, _('Internal')),
        (VISIBILITY_CHOICE_PUBLIC, _('Public')),
    )
    visibility = models.CharField(_('Visibility'), max_length=15, choices=VISIBILITY_CHOICE, default=VISIBILITY_CHOICE_INTERNAL, null=False, blank=False)

    EVALUATION_TYPE_CHOICE_SINGLE = 'single'
    EVALUATION_TYPE_CHOICE_PEER = 'peer'
    EVALUATION_TYPE_CHOICE = (
        (EVALUATION_TYPE_CHOICE_SINGLE, _('Single')),
        (EVALUATION_TYPE_CHOICE_PEER, _('Peer'))
    )
    evaluation_type = models.CharField(_('Evaluation Type'), max_length=255, choices=EVALUATION_TYPE_CHOICE, null=True, blank=False)

    consultant = models.CharField(_('Consultant'), max_length=60, blank=True, null=True)
    auditor = models.CharField(_('Auditor'), max_length=60, blank=True, null=True)
    accompanying_consultant = models.CharField(_('Accompanying Consultant'), max_length=60, blank=True, null=True)

    peer_companies = models.ManyToManyField('ecg_balancing.Company', verbose_name=_('Peer Companies'), max_length=255, blank=True, null=True)

    EMPLOYEES_NUMBER_CHOICE_ONE = 'one'
    EMPLOYEES_NUMBER_CHOICE_TWO = 'two'
    EMPLOYEES_NUMBER_CHOICE_THREE = 'three'
    EMPLOYEES_NUMBER_CHOICE_FOUR = 'four'
    EMPLOYEES_NUMBER_CHOICE_FIVE = 'five'
    EMPLOYEES_NUMBER_CHOICE_SIX = 'six'
    EMPLOYEES_NUMBER_CHOICE_SEVEN = 'seven'
    EMPLOYEES_NUMBER_CHOICE_EIGHT = 'eight'
    EMPLOYEES_NUMBER_CHOICE_NINE = 'nine'
    EMPLOYEES_NUMBER_CHOICE_TEN = 'ten'
    EMPLOYEES_NUMBER_CHOICE_ELEVEN = 'eleven'
    EMPLOYEES_NUMBER_CHOICE_TWELVE = 'twelve'
    EMPLOYEES_NUMBER_CHOICE_THIRTEEN = 'thirteen'
    EMPLOYEES_NUMBER_CHOICE_FOURTEEN = 'fourteen'

    EMPLOYEES_NUMBER_CHOICES = (
        (EMPLOYEES_NUMBER_CHOICE_ONE, _('1 employee')),
        (EMPLOYEES_NUMBER_CHOICE_TWO, _('2 employees')),
        (EMPLOYEES_NUMBER_CHOICE_THREE, _('3-5 employees')),
        (EMPLOYEES_NUMBER_CHOICE_FOUR, _('6-10 employees')),
        (EMPLOYEES_NUMBER_CHOICE_FIVE, _('11-20 employees')),
        (EMPLOYEES_NUMBER_CHOICE_SIX, _('21-50 employees')),
        (EMPLOYEES_NUMBER_CHOICE_SEVEN, _('51-100 employees')),
        (EMPLOYEES_NUMBER_CHOICE_EIGHT, _('101-200 employees')),
        (EMPLOYEES_NUMBER_CHOICE_NINE, _('201-350 employees')),
        (EMPLOYEES_NUMBER_CHOICE_TEN, _('351-500 employees')),
        (EMPLOYEES_NUMBER_CHOICE_ELEVEN, _('501-750 employees')),
        (EMPLOYEES_NUMBER_CHOICE_TWELVE, _('751-1.000 employees')),
        (EMPLOYEES_NUMBER_CHOICE_THIRTEEN, _('1.001-1.500 employees')),
        (EMPLOYEES_NUMBER_CHOICE_FOURTEEN, _('1.501-2.500 employees')),
    )
    employees_number = models.CharField(_('Number of employees'), max_length=255, choices=EMPLOYEES_NUMBER_CHOICES)
    
    revenue = models.IntegerField(_('Revenue'), blank=False, null=True)
    profit = models.IntegerField(_('Profit'), blank=False, null=True)

    worked_hours = models.PositiveSmallIntegerField(_('Worked Hours'), blank=False, null=True)
    number_participated_employees = models.PositiveSmallIntegerField(_('Number of participated employees'), blank=False, null=True)

    common_good = models.TextField(_('The Company and Common Good'), blank=True, null=True)
    prospect = models.TextField(_('Prospect'), blank=False, null=True)
    process_description = models.TextField(_('Balance process description'), blank=False, null=True)
    internal_communication = models.TextField(_('How was the balance internally communicated?'), blank=False, null=True)

    class Meta:
        verbose_name = _('Year Balance')
        verbose_name_plural = _('Year Balances')

    def is_sole_proprietorship(self):
        return self.employees_number == 'one'

    def __unicode__(self):
        return '%s:%s:%s' % (
            unicode(self.company),
            unicode(self.matrix),
            unicode(self.year)
        )

    def recalculate_points(self):
        calculated_points = 0
        balance_indicators = CompanyBalanceIndicator.objects.filter(company_balance=self, indicator__parent=None)
        for balance_indicator in balance_indicators:
            balance_indicator_evaluation = balance_indicator.evaluation
            if balance_indicator_evaluation != 0:
                calculated_points += balance_indicator_evaluation

        if self.is_sole_proprietorship:
            calculated_points = int (round (calculated_points * (float (1000) / 790) ))

        self.points = calculated_points


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

    description = models.TextField(_('Target questions'), blank=True, null=True)
    key_figures = models.TextField(_('Key figures'), blank=True, null=True)
    evaluation_table = models.TextField(_('Evaluation table'), blank=True, null=True)
    evaluation = models.IntegerField(_('Evaluation'), default=0)
    relevance = models.CharField(_('Relevance'), max_length=10, choices=Indicator.RELEVANCE_VALUES, blank=False, null=False)
    relevance_comment = models.TextField(_('Relevance comment'), blank=True, null=True)

    objects = CompanyBalanceIndicatorManager()

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


class UserRole(models.Model):
    ROLE_CHOICE_PENDING = 'pending'
    ROLE_CHOICE_NONE = 'none'
    ROLE_CHOICE_MEMBER = 'member'
    ROLE_CHOICE_ADMIN = 'admin'
    ROLE_CHOICES = (
        (ROLE_CHOICE_PENDING, _('Pending')),
        (ROLE_CHOICE_NONE, _('Not a member')),
        (ROLE_CHOICE_MEMBER, _('Member')),
        (ROLE_CHOICE_ADMIN, _('Admin')),
    )

    company = models.ForeignKey('ecg_balancing.Company', verbose_name=_('Company'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('User'), related_name='role')
    role = models.CharField(_('Role'), max_length=10, choices=ROLE_CHOICES)

    class Meta:
        verbose_name = _('User Role')
        verbose_name_plural = _('User Roles')

    def __unicode__(self):
        return "%s:%s:%s" % (
            unicode(self.company),
            unicode(self.user),
            unicode(self.role)
        )


class FeedbackIndicator(models.Model):
    indicator = models.ForeignKey('ecg_balancing.Indicator', verbose_name=_('Indicator'), related_name="feedback")
    sender_name = models.CharField(_('Sender Name'), max_length=255)
    sender_email = models.EmailField(_('Sender Email'))
    receiver_name = models.CharField(_('Receiver Name'), max_length=255, blank=True, null=True)
    receiver_email = models.EmailField(_('Receiver Email'), blank=True, null=True)
    message = models.TextField(_('Feedback'))

    class Meta:
        verbose_name = _('Feedback Indicator')
        verbose_name_plural = _('Feedback Indicators')

    def __unicode__(self):
        return "%s: %s"%(self.indicator, self.sender_name)