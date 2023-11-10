from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def confirm_order(user, orders, address):
    context = {
        "orders": orders,
        "user": user,
        "address": address
    }
    template_name = "email/confirm.html"
    convert_to_html_content = render_to_string(template_name=template_name, context=context)
    message = strip_tags(convert_to_html_content)

    send_mail(
        subject="Email Validation from Docollective",
        message=message,
        recipient_list=[user.email],
        from_email=None
    )
