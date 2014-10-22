from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

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


class FeedbackIndicatorAdmin(admin.ModelAdmin):
    pass


admin.site.register(FeedbackIndicator, FeedbackIndicatorAdmin)


class UserRoleAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserRole, UserRoleAdmin)


# user / user profile related admin

USER_MODEL = get_user_model()


class UserProfileInline(admin.StackedInline):
    model = UserProfile


class UserAdmin(DjangoUserAdmin):
    inlines = (UserProfileInline,)

admin.site.unregister(USER_MODEL)
admin.site.register(USER_MODEL, UserAdmin)
