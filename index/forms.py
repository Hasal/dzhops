# -*- coding: utf-8 -*-

from django import forms

class UploadFileForm(forms.Form):
    '''
    Upload user picture for profile web.
    '''
    file = forms.FileField(required=False)

class ChangePasswordForms(forms.Form):
    '''
    change password for user;
    '''
    password_old = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_new = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_new_again = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_password_new_again(self):
        password_new = self.cleaned_data['password_new']
        password_new_again = self.cleaned_data['password_new_again']
        if password_new_again != password_new:
            raise forms.ValidationError(u"新密码不一致！")
        return password_new, password_new_again