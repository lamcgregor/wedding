import floppyforms as forms

class UserForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=255, required=True)
    last_name = forms.CharField(label='Last Name', max_length=255, required=True)
    email = forms.EmailField(label='Email Address', required=False)

class RsvpForm(forms.Form):
    attending = forms.ChoiceField(choices=[('', 'Please Choose...'), ('yes', 'Yes'), ('no', 'No')], required=True)
