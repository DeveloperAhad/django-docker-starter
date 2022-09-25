from django.conf import settings
from backend import celery_app
from django.template.loader import render_to_string
from django.core.mail import EmailMessage


@celery_app.task()
def send_account_reset_password_email(to, context, from_email=settings.DEFAULT_FROM_EMAIL):
    html_version = 'account/email/email-reset-password.html'
    html_message = render_to_string(html_version, context=context)
    email_subject = 'Reset Password'
    message = EmailMessage(email_subject, html_message, from_email, [to])
    message.content_subtype = 'html'
    message.send()
