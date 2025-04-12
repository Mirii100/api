from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile, Order, OrderItem, Notification

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=Order)
def order_status_notification(sender, instance, created, **kwargs):
    if not created and instance.status == 'shipped':
        Notification.objects.create(
            user=instance.user,
            title="Order Shipped",
            message=f"Your order #{instance.id} has been shipped!"
        )
    elif not created and instance.status == 'delivered':
        Notification.objects.create(
            user=instance.user,
            title="Order Delivered",
            message=f"Your order #{instance.id} has been delivered!"
        )
