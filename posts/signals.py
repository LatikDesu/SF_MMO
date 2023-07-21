from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from posts.models import Comment
from posts.tasks import send_email_to_user, send_email_to_author


@receiver(pre_save, sender=Comment)
def on_change(sender, instance: Comment, **kwargs):
    if instance.id is not None:
        previous = Comment.objects.get(id=instance.id)
        if previous.rev_status != instance.rev_status:
            send_email_to_user.delay(instance.pk)


@receiver(post_save, sender=Comment)
def my_handler(sender, instance, created, **kwargs):
    if created:
        send_email_to_author.delay(instance.pk)
