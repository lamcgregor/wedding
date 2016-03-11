from django import forms

class RsvpForm(forms.Form):
    full_name = forms.CharField(label='Full Name', max_length=255, required=True)
    email = forms.EmailField(label='Email Address', required=True)
