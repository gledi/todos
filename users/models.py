from django.db import models
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.contrib.auth.models import AbstractUser
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.template.loader import render_to_string


class User(AbstractUser):
    phone = models.CharField(_("phone"), max_length=10)

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        db_table = 'users'
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self) -> str:
        return self.username


class Activation(models.Model):
    user = models.ForeignKey(User, verbose_name=_('user'), on_delete=models.CASCADE)
    activation_key = models.CharField(_("activation key"), max_length=255, unique=True)
    is_used = models.BooleanField(_("is used?"), default=False)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        db_table = 'activations'
        verbose_name = _("activation")
        verbose_name_plural = _("activations")

    def __str__(self) -> str:
        return f'Activation: {self.user}'

    def generate_email_message(self, request: HttpRequest) -> EmailMessage:
        message = EmailMultiAlternatives()
        url = request.build_absolute_uri(
            reverse('activate', kwargs={'activation_key': self.activation_key})
        )

        context = {
            "name": self.user.get_full_name(),
            "activation_url": url,
            "activation_period": 7,
        }
        text_body = render_to_string(
            "users/activation_email.txt",
            context=context,
        )
        html_body = render_to_string(
            "users/activation_email.html",
            context=context,
        )
        message = EmailMultiAlternatives(
            subject="Activate your account",
            from_email="noreply@todos.al",
            to=[self.user.email],
            body=text_body,
        )
        message.attach_alternative(html_body, "text/html")
        return message
