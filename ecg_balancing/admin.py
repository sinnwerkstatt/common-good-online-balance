from django.contrib import admin

from ecg_balancing.models import *

class ECGMatrixAdmin(admin.ModelAdmin):
	pass
admin.site.register(ECGMatrix, ECGMatrixAdmin)
class IndicatorAdmin(admin.ModelAdmin):
	pass
admin.site.register(Indicator, IndicatorAdmin)
class CompanyAdmin(admin.ModelAdmin):
	pass
admin.site.register(Company, CompanyAdmin)
class CompanyBalanceAdmin(admin.ModelAdmin):
	pass
admin.site.register(CompanyBalance, CompanyBalanceAdmin)
class CompanyBalanceIndicatorAdmin(admin.ModelAdmin):
	pass
admin.site.register(CompanyBalanceIndicator, CompanyBalanceIndicatorAdmin)
class UserRoleAdmin(admin.ModelAdmin):
	pass
admin.site.register(UserRole, UserRoleAdmin)