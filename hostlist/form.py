# -*- coding: utf-8 -*-
from django import forms
from hostlist.models import *


class HostsListForm(forms.ModelForm):
    class Meta:
        model = HostList
        widgets = {
            'hostname': forms.TextInput(attrs={'class': 'form-control'}),
            'ip': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'dc_cn': forms.TextInput(attrs={'class': 'form-control'}),
            'engineer': forms.TextInput(attrs={'class': 'form-control'}),
            'mac_addr': forms.TextInput(attrs={'class': 'form-control'}),
            'main_source_ip': forms.TextInput(attrs={'class': 'form-control'}),
            'backup_source_ip': forms.TextInput(attrs={'class': 'form-control'}),
            'lic_date': forms.TextInput(attrs={'class': 'form-control'}),
            'lic_status': forms.TextInput(attrs={'class': 'form-control'}),
            'remark': forms.TextInput(attrs={'class': 'form-control'}),
        }
