from django.db.models import Manager


class CompanyBalanceIndicatorManager(Manager):
	def get_by_parent(self, parent):
		return self.filter(indicator__parent=parent.indicator, company_balance=parent.company_balance)
            
    #def get_by_indicator_pk(self, indicator_pk):
    #    return self.get(indicator=indicator_pk)

    #def get_by_indicator_pks(self, indicator_pks, company):
    #    return self.filter(indicator__pk__in=indicator_pks, company_balance__company=company).all()

#CompanyBalanceIndicator.objects.get_company_balance_indicator(indicatorId)

class CompanyManager(Manager):
    def as_choices(self):
        for company in self.all():
            yield (company.pk, unicode(company))
