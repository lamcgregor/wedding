document.addEventListener 'DOMContentLoaded', ->
    rsvpForm = document.querySelector('.js-rsvp-form');
    if rsvpForm
        httpRequest = new XMLHttpRequest();
        httpRequest.open('GET', '/api/rsvp', true);
        httpRequest.send(null);
        httpRequest.onreadystatechange = ->
            if httpRequest.readyState == 4 and httpRequest.status == 200
                console.log httpRequest.responseText
                rsvpForm.innerHTML = httpRequest.responseText
                formElem = rsvpForm.getElementsByTagName('form')[0]
                console.log formElem
                formElem.addEventListener 'submit', (e) ->
                    e.preventDefault()
                    fields = this.getElementsByTagName('input')
                    for i in fields
                        console.log i