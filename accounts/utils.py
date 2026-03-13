from django.shortcuts import redirect
from django.core.mail import send_mail
from django.conf import settings
import threading

def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        return view_func(request, *args, **kwargs)
    return wrapper


def send_email_thread(subject, message, recipient_email):
    """Email yuborishni alohida threadda bajaradi.
    Sahifa "muzlab" qolmaydi — foydalanuvchi kutmaydi."""

    def _send():
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[recipient_email],
            fail_silently=False,
        )

    thread = threading.Thread(target=_send)
    thread.daemon = True
    thread.start()