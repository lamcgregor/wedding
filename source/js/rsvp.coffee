$(document).ready ->
    dietary_toggle = ->
        if @.value == 'other'
            $(this).parent().find('.dietary-other-field').show().attr('required', 'true')
        else
            $(this).parent().find('.dietary-other-field').hide().removeAttr('required')

    rsvpForm = $('.js-rsvp-form');
    if rsvpForm.length > 0
        $.ajax
            url: '/api/rsvp/user'
            type:'GET'
            success: (response) ->
                rsvpForm.html response['content']
                dietary_toggle.call(rsvpForm.find('.dietary-requirements-field')[0])

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

        $(document).on 'change', '.js-rsvp-form .dietary-requirements-field', dietary_toggle
