from django.shortcuts import render

from django.http import HttpResponseRedirect
from django.core import urlresolvers

from .forms import GuestForm, RsvpForm
from .models import Guest

def get_guest(request):
    if 'guest_id' not in request.session:
        return None
    return Guest.filter(id=request.session['guest_id']).first()

def rsvp_form(request):
    if request.method == 'POST':
        form = RsvpForm(request.POST)
        import pdb
        pdb.set_trace()
        if form.is_valid():
            return HttpResponseRedirect('/thanks/')

    form = RsvpForm(initial={'guest': Guest.objects.get(id=request.session['guest_id'])})

    return render(request, 'rsvp/rsvp_form.html', {'form': form})

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
                form.add_error("No guest matches name, please ensure it is spelt the same as your invitation")
            else:
                guest = guests.first()
                request.session['guest_id'] = guest.id

            if form.is_valid():
                return render(request, 'rsvp/rsvp_form.html', {'form': form})
            else:
                return render(request, 'rsvp/guest_form.html', {'form': form})

    form = GuestForm()

    return render(request, 'rsvp/guest_form.html', {'form': form})
