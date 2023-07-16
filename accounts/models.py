from django.contrib.auth.models import AbstractUser, Group
from django.core.mail import EmailMultiAlternatives, send_mail
from django.db import models
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.timezone import now

from SF_MMORPG import settings


class User(AbstractUser):
    image = models.ImageField(upload_to='users', null=True, blank=True,
                              default='users/default_avatar.jpg')
    is_verified_email = models.BooleanField(default=False)
    about = models.TextField(blank=True)
    role = models.CharField(max_length=100, default='no class')

    def __str__(self):
        return f'{self.username} - {self.role}'

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

        app_label = 'accounts'


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def __str__(self):
        return f'EmailVerification object for {self.user.email}'

    def send_verification_email(self):
        link = reverse('users:email_verification', kwargs={'email': self.user.email, 'code': self.code})
        verification_link = f'{settings.DOMAIN_NAME}{link}'
        subject = f'Подтверждение учетной записи для {self.user.username}'
        message = 'Для подтверждения учетной записи для {} перейдите по ссылке: {}'.format(
            self.user.email,
            verification_link
        )

        html_content = render_to_string(
            'mail/email_verification.html',
            {
                'username': self.user.username,
                'verification_link': verification_link,
            }
        )

        msg = EmailMultiAlternatives(
            subject=subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[self.user.email],
        )
        msg.attach_alternative(html_content, "text/html")

        msg.send()

    def is_expired(self):
        return True if now() >= self.expiration else False
