import threading
from django.core.mail import send_mail
from django.conf import settings


def send_order_confirmation_email(order_id, user_email, total_price):
    def _send():
        send_mail(
            subject=f'Order #{order_id} confirmed',
            message=f'Thank you for your order!\n\nOrder #{order_id}\nTotal: Rs.{total_price}\n\nWe will ship it soon.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            fail_silently=False,
        )
    thread = threading.Thread(target=_send)
    thread.daemon = True
    thread.start()