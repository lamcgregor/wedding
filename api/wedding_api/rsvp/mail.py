from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings


def send_update_mail(changes, user):
    if not changes:
        return

    try:
        if len(changes) > 3:
            subject = ', '.join(list(g.first_name for g in changes.keys())[:2])
            subject += ', and {} others'.format(len(list(changes.keys())[2:]))
        else:
            subject = ', '.join(g.first_name for g in changes.keys())

        if len(changes) == 1:
            subject += ' has RSVP\'d'
        else:
            subject += 'have RSVP\'d'

        if settings.ENVIRONMENT != 'production':
            subject = 'TEST EMAIL (from {}): '.format(settings.ENVIRONMENT) + subject

        send_mail(subject, render_to_string('rsvp/update_email.txt', {'changes': changes, 'user': user}),
                  'notifications@lukeandpeggy.com',
                  ['lawoollett@gmail.com'],
                  fail_silently=False)

    except Exception as e:
        pass
