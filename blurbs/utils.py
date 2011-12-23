from django.core.mail import EmailMessage
from django.template.loader import render_to_string

def send_email(subject, template, to, subject_prefix='[EUS Pipeline] ',
               template_prefix='emails/', **kwargs):
    message = render_to_string(template_prefix + template, kwargs)
    email = EmailMessage(subject_prefix + subject, message, to=to)
    email.content_subtype = 'html'
    email.send()
