from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    # posts

    def __str__(self):
        return self.name


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
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='posts')

    # user_id

    def __str__(self):
        return self.caption
