$(document).ready ->
    rsvpForm = $('.js-rsvp-form');
    if rsvpForm.length > 0
        $.ajax
            url: '/api/rsvp/user'
            type:'GET'
            success: (response) ->
                rsvpForm.html response['content']
        $(document).on 'submit', 'form', (e) ->
            e.preventDefault()
            $this = $(this)
            content = $this.serialize $this
            $.post $this.attr('action'),content, (response) ->
                if response['content']
                    $this
                        .parent()
                        .html response['content']
                else if response['redirect']
                    location.href = response['redirect']
