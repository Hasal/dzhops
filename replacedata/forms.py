# -*- coding: utf-8 -*-
from django import forms
import re

class RedataAllForms(forms.Form):
    '''
    forms for data_replace_all.html
    '''

    data_source = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    data_path = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    target_server = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean_data_source(self):
        '''
        checkout ip address lawful
        :return:
        '''
        pattern = re.compile(
            r'(\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b)')
        data_source = self.cleaned_data['data_source']
        mth = pattern.match(data_source)
        if not mth:
            raise forms.ValidationError(u"IP地址格式不合法！")
        return data_source
