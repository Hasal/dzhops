# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.
from saltstack.models import DangerCommand, ModulesLock, DeployModules, ConfigUpdate, CommonOperate

admin.site.register(DangerCommand)
admin.site.register(ModulesLock)
admin.site.register(DeployModules)
admin.site.register(ConfigUpdate)
admin.site.register(CommonOperate)
