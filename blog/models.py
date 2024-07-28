from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.functional import cached_property
from mistune import markdown


class Post(models.Model):
    title = models.CharField(_("title"), max_length=256)
    slug = models.SlugField(_("slug"), max_length=256)
    body = models.TextField(_("body"))
    is_published = models.BooleanField(_("is published"), default=False)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("author"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts",
    )

    class Meta:
        db_table = "posts"
        verbose_name = _("post")
        verbose_name_plural = _("posts")
        indexes = [
            models.Index(fields=["slug"]),
        ]
        permissions = [
            ("publish_post", _("Can publish post")),
        ]

    def __str__(self) -> str:
        return self.title

    @cached_property
    def body_html(self) -> str:
        return markdown(self.body)
