from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Post(models.Model):
    title = models.CharField(_("title"), max_length=256)
    slug = models.SlugField(_("slug"), max_length=256)
    body = models.TextField(_("body"))
    rate = models.IntegerField(_("rate"), default=1)
    is_published = models.BooleanField(_("is published"), default=False)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("author"),
                               on_delete=models.SET_NULL,
                               null=True, blank=True, related_name='posts')

    class Meta:
        db_table = 'posts'
        verbose_name = _('post')
        verbose_name_plural = _('posts')
        indexes = [
            models.Index(fields=['slug']),
        ]
        constraints = [
            models.CheckConstraint(check=models.Q(rate__gte=1) & models.Q(rate__lte=10), name="chk_posts_rate"),
        ]

    def __str__(self):
        return self.title
