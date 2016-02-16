from django.contrib import admin

# Register your models here.
from replacedata.models import StockExchage,StockIndex

# Register your models here.

admin.site.register(StockExchage)
admin.site.register(StockIndex)
