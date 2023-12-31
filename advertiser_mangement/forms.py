from django import forms

class InputForm(forms.Form):
    advertiser_id = forms.IntegerField()
    image = forms.ImageField()
    title = forms.CharField(max_length = 200)
    url = forms.CharField(max_length = 200)
