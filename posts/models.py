from django.db import models
from django.conf import settings
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class Post(models.Model):
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/')
    photo_thumbnail = ImageSpecField(source='photo',
                                     processors=[ResizeToFill(84, 84)],
                                     format='JPEG',
                                     options={'quality': 60})
    photo_single = ImageSpecField(source='photo',
                                  processors=[ResizeToFill(600, 400)],
                                  format='JPEG',
                                  options={'quality': 80})
    caption = models.TextField(blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='posts')

    # user_id

    def __str__(self):
        return self.caption
