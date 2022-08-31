from django.core.mail import EmailMessage
from django.utils import timezone
from datetime import datetime



def send_mail(data):
    mail = EmailMessage(
        subject=data['email_subject'],
        body=data['email_body'],
        from_email=data['from_email'],
        to=data['to_email']
    )
    return mail.send()


def get_now() -> datetime:
    return timezone.now()


def get_first_matching_attr(obj, *attrs, default=None):
    for attr in attrs:
        if hasattr(obj, attr):
            return getattr(obj, attr)

    return default


def get_error_message(exc) -> str:
    if hasattr(exc, 'message_dict'):
        return exc.message_dict
    error_msg = get_first_matching_attr(exc, 'message', 'messages')

    if isinstance(error_msg, list):
        error_msg = ', '.join(error_msg)

    if error_msg is None:
        error_msg = str(exc)

    return error_msg
