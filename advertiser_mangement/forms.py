from collections.abc import Mapping
from typing import Any
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class InputForm(forms.Form):
    advertiser_ID = forms.IntegerField()
    image = forms.ImageField()
    title = forms.CharField(max_length = 200)
    url = forms.CharField(max_length = 200)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit', 'Create Ad'))
