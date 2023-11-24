from django.core.management.base import BaseCommand, CommandError
from django.core.mail import EmailMessage
from shop.models import Order
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = "Re send an email to users who ordered more than 15 days ago and whose order is not validated"

    def handle(self, *args, **options):
        try:
            orders = Order.objects.filter(ordered_date__lt=timezone.now() - timedelta(days=15))
            for order in orders:
                subject = f"Docoville, commande {order.reference}"
                receiver = order.user.email
                content = (f"Bonjour, nous n'avons toujours pas reçu votre "
                           f"vêtement en échange de {order.garment.description}. Cordialement")
                email = EmailMessage(
                    subject, content, 'gabrieltrouve5@gmail.com', [receiver]
                )
                email.send()
                print(f"Mail envoyé pour la commande {order.reference} de {order.user.email}")
        except Exception as e:
            raise CommandError(e)
