# coding: utf-8

from django import forms


class DingDingOptionsForm(forms.Form):
    access_token = forms.CharField(
        max_length=255,
        help_text='钉钉机器人的access_token'
    )
    keyword = forms.CharField(
        max_length=255,
        help_text='钉钉机器人的keyword'
    )
    secret = forms.CharField(
        max_length=255,
        help_text='钉钉机器人的secret'
    )
    
