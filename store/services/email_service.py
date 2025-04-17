import threading
import logging

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site

from store.services.token_service import account_activation_token


def send_activation_email(request, user):
    try:
        current_site = get_current_site(request)
        mail_subject = "Activate your account."
        message = render_to_string(
            "registration/emails/acc_active_email.html",
            {
                "user": user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user),
            },
        )

        email = EmailMessage(mail_subject, message, to=[user.email])
        email.content_subtype = "html"

        threading.Thread(target=email.send).start()

    except Exception as e:
        logging.error(f"Error sending activation email: {e}")
        raise
