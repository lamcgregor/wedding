import floppyforms as forms

from django.forms import formset_factory
from .models import Guest

class GuestForm(forms.Form):
    first_name = forms.CharField(label='First name', max_length=255, required=True)
    last_name = forms.CharField(label='Last name', max_length=255, required=True)

class RsvpForm(forms.Form):
    attending = forms.ChoiceField(choices=[('', 'Please choose...'), ('yes', 'Yes'), ('no', 'No')], required=False)
    email = forms.EmailField(label='Email address', required=False)
    dietary_requirements = forms.ChoiceField(
        choices=[
            ('', 'No special requirements'), 
            ('vegetarian', 'Vegetarian'), 
            ('vegan', 'Vegan'), 
            ('other', 'Other')
        ], 
        required=False,
        widget=forms.Select(attrs={'class': 'dietary-requirements-field'}))

    dietary_other = forms.CharField(label='', widget=forms.Textarea(
        attrs={
            'placeholder': 'Please specify', 
            'class': 'dietary-other-field', 
            'rows': 5}
        ), 
        required=False)
    comments = forms.CharField(label='Comments', widget=forms.Textarea(
        attrs={
            'rows': 3}
        ), 
        required=False)
    guest = forms.ModelChoiceField(queryset=Guest.objects.none(), label='Test', widget=forms.HiddenInput())

RsvpFormSet = formset_factory(RsvpForm, extra=0)