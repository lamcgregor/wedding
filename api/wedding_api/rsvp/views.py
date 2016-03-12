from django.shortcuts import render

from django.http import HttpResponseRedirect

from .forms import RsvpForm

def form(request):
    if request.method == 'POST':
        form = RsvpForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/thanks/')

    form = RsvpForm()

    return render(request, 'rsvp/form.html', {'form': form})
