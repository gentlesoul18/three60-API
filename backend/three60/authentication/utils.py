from django.core.mail import EmailMessage


def send_mail(data):
    mail = EmailMessage(
        subject=data['email_subject'],
        body=data['email_body'],
        from_email=data['from_email'],
        to=data['to_email']
    )
    return mail.send()