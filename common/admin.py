from django.contrib import admin
from common.models import OperateRecord, ReturnRecord, DeployModules, ConfigUpdate, CommonOperate, ModulesLock
# Register your models here.

admin.site.register(OperateRecord)
admin.site.register(ReturnRecord)
admin.site.register(DeployModules)
admin.site.register(ConfigUpdate)
admin.site.register(CommonOperate)
admin.site.register(ModulesLock)