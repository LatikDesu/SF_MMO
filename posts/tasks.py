from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from SF_MMORPG import settings
from posts.models import Post, Comment


@shared_task
def send_email_to_user(pk):
    comment = Comment.objects.get(id=pk)
    post = comment.post
    user = comment.user

    link = f'{settings.DOMAIN_NAME}{post.get_absolute_url()}'

    html_content = render_to_string(
        'mail/email_comment_status.html',
        {
            'title': post.title,
            'link': link
        }
    )

    msg = EmailMultiAlternatives(
        subject=f"MMORPG| Ваш отклик принят!",
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=user.email,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def send_email_to_author(pk):
    comment = Comment.objects.get(id=pk)
    post = comment.post
    user = post.user

    link = f'{settings.DOMAIN_NAME}{post.get_absolute_url()}'

    html_content = render_to_string(
        'mail/email_comment_add.html',
        {
            'title': post.title,
            'link': link
        }
    )

    msg = EmailMultiAlternatives(
        subject=f"MMORPG| У вас новый отклик!",
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=user.email,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()
