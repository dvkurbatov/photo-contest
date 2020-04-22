from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import os



class Photo(models.Model):
  title = models.CharField(max_length=50)
  image = models.FileField(upload_to='images/')
  thumbnail = models.FileField(upload_to='thumbs/', null=True)
  author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

  created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

  def get_absolute_url(self):
    return reverse('show_photo', args=[str(self.id)])

  def save(self, *args, **kwargs):
    super(Photo, self).save(*args, **kwargs)
    self.make_thumb()

  def make_thumb(self):
    img = Image.open(self.image)
    img.thumbnail((250, 200))

    thumb_name, thumb_extension = os.path.splitext(self.image.name)
    thumb_filename = thumb_name + '_thumb' + thumb_extension
    temp_handle = BytesIO()
    img.save(temp_handle, 'JPEG')
    #temp_thumb.seek(0)
    breakpoint()
    self.thumbnail.save(thumb_filename, ContentFile(temp_handle.read()), save=False)
    temp_handle.close()

    return True


class Like(models.Model):
  user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
  photo = models.ForeignKey(Photo, on_delete=models.CASCADE)

  created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)

  class Meta:
    unique_together = ('user_id', 'photo_id',)