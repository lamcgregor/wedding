from django.template.loader import render_to_string

from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.core import urlresolvers

from .forms import GuestForm, RsvpFormSet
from .models import Guest

def get_guest(request):
    if 'guest_id' not in request.session:
        return None
    return Guest.filter(id=request.session['guest_id']).first()

def rsvp_form(request):
    guest = Guest.objects.get(id=request.session['guest_id'])
    if guest.group:
        guests = guest.group.guest_set.order_by("last_name", "first_name")
    else:
        guests = [guest]

    if request.method == 'POST':
        formset = RsvpFormSet(request.POST)
        # Only allow submitter to change allowed guests
        for form in formset:
            form.fields['guest'].queryset = guests
        if form.is_valid():
            for form in formset:
                form.full_clean()
                guest = form.clean()['guest']
                guest.attending = form.clean()['attending']
                guest.email = form.clean()['email']
                guest.save()

            return JsonResponse({
                'redirect': '/thanks'
            })
        else:
            for form in formset:
                form.initial = {'guest': Guest.objects.get(id=form['guest'].value())}
    else:
        formset = RsvpFormSet(initial=[{'guest': g, 'email': g.email, 'attending': g.attending} for g in guests])



    return JsonResponse({
        'content': render_to_string('rsvp/rsvp_form.html', {'rsvp_formset': formset, 'action': urlresolvers.reverse('rsvp-form')}, request=request)
    })

def guest_form(request):
    if 'guest_id' in request.session:
        return HttpResponseRedirect(urlresolvers.reverse('rsvp-form'))

    if request.method == 'POST':
        form = GuestForm(request.POST)
        if form.is_valid():
            guests = Guest.objects.filter(
                first_name__iexact=form.cleaned_data['first_name'],
                last_name__iexact=form.cleaned_data['last_name'])

            if len(guests) < 1:
                form.add_error("__all__", "No guest matches name, please ensure it is spelt the same as your invitation")
            else:
                guest = guests.first()
                request.session['guest_id'] = guest.id

            if form.is_valid():
                return  JsonResponse({
                    'redirect': urlresolvers.reverse('rsvp-form')
                })
            else:
                return JsonResponse({
                    'content': render_to_string('rsvp/form.html', {'form': form, 'action': urlresolvers.reverse('guest-form')}, request=request)
                })

    form = GuestForm()

    return JsonResponse({
        'content': render_to_string('rsvp/form.html', {'form': form, 'action': urlresolvers.reverse('guest-form')}, request=request)
    })
