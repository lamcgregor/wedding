from django.shortcuts import render

from django.http import HttpResponseRedirect

from .forms import UserForm, RsvpForm

def rsvp_form(request):
    if request.method == 'POST':
        form = RsvpForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/thanks/')

    form = RsvpForm()

    return render(request, 'rsvp/rsvp_form.html', {'form': form})

def user_form(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            return render(request, 'rsvp/rsvp_form.html', {'form': form})

    form = UserForm()

    return render(request, 'rsvp/user_form.html', {'form': form})
