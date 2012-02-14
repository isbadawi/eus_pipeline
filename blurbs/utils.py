from django.core.mail import EmailMessage
from django.template import Context, Template
from blurbs.models import Email

def send_email(subject, label, to, prefix='[EUS Pipeline] ', **kwargs):
    template = Template(Email.objects.get(label=label).body)
    message = template.render(Context(kwargs))
    email = EmailMessage(prefix + subject, message, to=(to,))
    email.content_subtype = 'html'
    email.send()
