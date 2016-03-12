utils = 
    ajax = (type, url, content, callback) ->
        type ?= 'GET';
        url ?= '/api/rsvp'
        httpRequest = new XMLHttpRequest();
        httpRequest.open(type, url, true);
        httpRequest.send(null);
        httpRequest.onreadystatechange = ->
            if httpRequest.readyState == 4 and httpRequest.status == 200
                console.log "done"