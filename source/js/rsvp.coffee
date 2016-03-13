$(document).ready ->
    rsvpForm = $('.js-rsvp-form');
    if rsvpForm.length > 0
        $.ajax
            url: '/api/rsvp'
            type:'GET'
            success: (response) ->
                rsvpForm.html response
                $(document).on 'submit', '.js-rsvp-form form', (e) ->
                    e.preventDefault()
                    $this = $(this)
                    content = $this.serialize $this
                    $.post $this.attr('action'),content, (response) ->
                        if response
                            $this.html response
                    return
        return