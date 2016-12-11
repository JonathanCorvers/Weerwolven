from django.db.models import forms
from django.forms.forms import Sed

class MainSubscriber(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    age = forms.IntegerField(min_value=0)


