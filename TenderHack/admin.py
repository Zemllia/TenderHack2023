from django.contrib import admin

from TenderHack.models import Company, Subdivision, TenderItem, QuotationSession, Region, Tender, Contract, \
    ContractExecution


class TenderItemInline(admin.StackedInline):
    model = TenderItem
    extra = 1


class TenderAdmin(admin.ModelAdmin):
    inlines = [TenderItemInline]


admin.site.register(Company)
admin.site.register(Subdivision)
admin.site.register(QuotationSession)
admin.site.register(Region)
admin.site.register(Tender, TenderAdmin)
admin.site.register(Contract)
admin.site.register(ContractExecution)
