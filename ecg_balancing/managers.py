from django.db.models import Manager


class CompanyBalanceIndicatorManager(Manager):

    def get_by_indicator_pk(self, indicator_pk):
        return self.get(indicator=indicator_pk)

    def get_by_indicator_pks(self, indicator_pks):
        return self.filter(indicator__pk__in=indicator_pks).all()

#CompanyBalanceIndicator.objects.get_company_balance_indicator(indicatorId)

class CompanyManager(Manager):
    def as_choices(self):
        for company in self.all():
            yield (company.pk, unicode(company))
