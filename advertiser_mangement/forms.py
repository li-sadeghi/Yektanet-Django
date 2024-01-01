from django import forms

class InputForm(forms.Form):
    advertiser_id = forms.CharField(max_length=200)
    image = forms.CharField(max_length= 200)
    title = forms.CharField(max_length = 200)
    url = forms.CharField(max_length = 200)
