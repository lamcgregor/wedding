import floppyforms as forms
from django import forms as django_forms
from django.forms import formset_factory
from .models import Guest, Group


class GuestForm(forms.Form):
    first_name = forms.CharField(label='First name', max_length=255, required=True)
    last_name = forms.CharField(label='Last name', max_length=255, required=True)


class GuestInlineForm(django_forms.ModelForm):
    guest = forms.ModelChoiceField(queryset=Guest.objects.all(), required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.initial['guest'] = self.instance.id

    def clean(self, *args, **kwargs):
        super().clean(*args, **kwargs)
        self.cleaned_data['id'] = self.cleaned_data['guest']
        self.instance = self.cleaned_data['guest']
        if self.cleaned_data['DELETE']:
            self.cleaned_data['DELETE_RELATION'] = True
            self.cleaned_data['DELETE'] = False
        return self.cleaned_data

    def save(self, *args, **kwargs):
        if 'DELETE_RELATION' in self.cleaned_data and self.cleaned_data['DELETE_RELATION']:
            self.cleaned_data['group'].guest_set.remove(self.cleaned_data['id'])
        else:
            self.cleaned_data['group'].guest_set.add(self.instance)
        return self.instance

    class Meta:
        model = Guest
        fields = ['guest']


class RsvpForm(forms.Form):
    attending = forms.ChoiceField(choices=[('', 'Please choose...'), ('yes', 'Yes'), ('no', 'No')], required=False)
    email = forms.EmailField(label='Email address', required=False)
    dietary_requirements = forms.ChoiceField(
        choices=[
            ('none', 'No special requirements'),
            ('vegetarian', 'Vegetarian'),
            ('vegan', 'Vegan'),
            ('nopork', 'No pork'),
            ('other', 'Other')
        ],
        required=True,
        widget=forms.Select(attrs={'class': 'dietary-requirements-field'}))

    dietary_other = forms.CharField(label='', widget=forms.Textarea(
        attrs={
            'placeholder': 'Please specify',
            'class': 'dietary-other-field',
            'rows': 5}
    ),
        required=False)
    comments = forms.CharField(label='Comments',  widget=forms.Textarea(
        attrs={
            'placeholder': 'Please leave any messages here',
            'rows': 3}
    ),
        required=False)
    guest = forms.ModelChoiceField(queryset=Guest.objects.none(), widget=forms.HiddenInput(), required=True)

RsvpFormSet = formset_factory(RsvpForm, extra=0)
