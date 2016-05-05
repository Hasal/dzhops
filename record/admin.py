from django.contrib import admin

# Register your models here.
from record.models import ReturnRecord, OperateRecord

admin.site.register(ReturnRecord)
admin.site.register(OperateRecord)