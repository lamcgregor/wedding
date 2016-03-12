document.addEventListener 'DOMContentLoaded', ->

  httpRequest = new XMLHttpRequest();
  httpRequest.open('GET', '/api/rsvp', true);
  httpRequest.send(null);

  httpRequest.onreadystatechange = handler;

  handler = ->
    if httpRequest.readyState == XMLHttpRequest.DONE:
      document.getElementsByClassName('js-rsvp-form')[0]
