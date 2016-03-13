$(document).ready ->
    rsvpForm = $('.js-rsvp-form');
    if rsvpForm.length > 0
        $.ajax
            url: '/api/rsvp'
            type:'GET'
            success: (response) ->
                rsvpForm.html response
        $(document).on 'submit', 'form', (e) ->
            e.preventDefault()
            $this = $(this)
            content = $this.serialize $this
            $.post $this.attr('action'),content, (response) ->
                if response
                    $this
                        .parent()
                        .html response
                    return
            return
        return