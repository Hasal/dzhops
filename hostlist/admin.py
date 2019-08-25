from django.contrib import admin
from hostlist.models import HostList, DzhUser, DataCenter, NetworkOperator, ProvinceArea, Category

# Register your models here.

admin.site.register(HostList)
admin.site.register(DzhUser)
admin.site.register(DataCenter)
admin.site.register(NetworkOperator)
admin.site.register(ProvinceArea)
admin.site.register(Category)