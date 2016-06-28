from django.template.loader import render_to_string

from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.core import urlresolvers

from django.db.models import Q
from django.db.models import Case, When

from .forms import GuestForm, RsvpFormSet
from .models import Guest


def get_guest(request):
    if 'guest_id' not in request.session:
        return None
    return Guest.filter(id=request.session['guest_id']).first()


def rsvp_form(request):
    guest_query = Guest.objects.filter(id=request.session['guest_id'])
    guest = guest_query.first()

    if guest.group:
        # Use case/when to force currently logged in guest to be first
        guests = guest.group.guest_set.order_by(Case(When(id=guest.id, then=0), default=1), "last_name", "first_name")
    else:
        guests = guest_query

    if request.method == 'POST':
        formset = RsvpFormSet(request.POST)
        for form in formset:
            form.fields['guest'].queryset = guests

        if form.is_valid():
            for form in formset:
                form.full_clean()
                guest = form.cleaned_data['guest']
                guest.attending = form.cleaned_data['attending']
                guest.email = form.cleaned_data['email']
                guest.dietary_requirements = form.cleaned_data['dietary_requirements']
                guest.dietary_other = form.cleaned_data['dietary_other']
                guest.comments = form.cleaned_data['comments']
                guest.save()

            return JsonResponse({
                'redirect': '/thanks'
            })
        else:
            for form in formset:
                form.initial = {'guest': Guest.objects.get(id=form['guest'].value())}
    else:
        formset = RsvpFormSet(initial=[{
            'guest': g,
            'email': g.email,
            'attending': g.attending,
            'comments': g.comments,
            'dietary_requirements': g.dietary_requirements,
            'dietary_other': g.dietary_other,
        } for g in guests])

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
                last_name__iexact=form.cleaned_data['last_name']
            ).exclude(last_name__isnull=True).exclude(last_name__exact='')

            if len(guests) < 1:
                form.add_error(
                    "__all__", "No guest matches name, please ensure it is spelt the same as your invitation. If you are having trouble logging in you can always RSVP by emailing p.h.mcgregor@gmail.com")
            else:
                guest = guests.first()
                request.session['guest_id'] = guest.id

            if form.is_valid():
                return HttpResponseRedirect(urlresolvers.reverse('rsvp-form'))
            else:
                return JsonResponse({
                    'content': render_to_string('rsvp/form.html', {'form': form, 'action': urlresolvers.reverse('guest-form')}, request=request)
                })

    form = GuestForm()

    return JsonResponse({
        'content': render_to_string('rsvp/form.html', {'form': form, 'action': urlresolvers.reverse('guest-form')}, request=request)
    })
