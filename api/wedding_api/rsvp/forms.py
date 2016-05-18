import floppyforms as forms

from django.forms import formset_factory
from .models import Guest

class GuestForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=255, required=True)
    last_name = forms.CharField(label='Last Name', max_length=255, required=True)

class RsvpForm(forms.Form):
    attending = forms.ChoiceField(choices=[('', 'Please Choose...'), ('yes', 'Yes'), ('no', 'No')], required=False)
    email = forms.EmailField(label='Email Address', required=False)
    dietary_requirements = forms.CharField(label='Dietary Requirements', widget=forms.TextInput(attrs={'placeholder': 'Vegetarian, Vegan, etc.'}))
    comments = forms.CharField(label='Comments')
    guest = forms.ModelChoiceField(queryset=Guest.objects.none(), label='Test', widget=forms.HiddenInput())

RsvpFormSet = formset_factory(RsvpForm, extra=0)