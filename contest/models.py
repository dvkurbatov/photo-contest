from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import os
from django.utils.html import mark_safe
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


def get_path(instance, filename):
  kind_image = 'thumbs' if filename[0:10] == 'v_300x200_' else 'images'
  file_path = 'photo/{}/{}/{}'.format(kind_image, instance.id, filename)
  return file_path

class Photo(models.Model):
  title = models.CharField(max_length=50)
  image = models.FileField(upload_to=get_path)
  thumb_for_gallery = models.FileField(upload_to=get_path, null=True)
  author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
  created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
  #likes_count = models.IntegerField(default=0)

  def image_tag(self):
    from django.utils.html import escape
    return mark_safe('<img src="%s" />'.format(self.thumb_for_gallery.url))

  def likes_count(self):
    return self.like_set.all().count()

  def get_absolute_url(self):
    return reverse('show_photo', args=[str(self.id)])

  def save(self, *args, **kwargs):
    if self.pk is None:
      saved_image = self.image
      self.image = None
      super(Photo, self).save(*args, **kwargs)
      self.image = saved_image

    extension = self.image.name.split('.')[-1]
    if extension in ['jpg', 'png']:
      self.image.name = "{}.{}".format(self.title, extension)
      self.make_gallery_thumb()
    super(Photo, self).save(*args, **kwargs)

  def make_gallery_thumb(self):
    size = (300, 200)
    original_image = Image.open(self.image.file)
    resized_image = original_image.resize(size)
    resized_image_filename = "v_300x200_{}".format(self.image.name)
    tmp_thumb = BytesIO()
    resized_image.save(tmp_thumb, 'JPEG')
    tmp_thumb.seek(0)
    self.thumb_for_gallery.save(resized_image_filename, ContentFile(tmp_thumb.read()), save=False)
    tmp_thumb.close()


class Like(models.Model):
  user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
  photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)

  class Meta:
    unique_together = ('user_id', 'photo_id',)


class Comment(models.Model):
  user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
  text = models.TextField(max_length=250)
  created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)
  commented_object_id = models.IntegerField(default=0)
  commented_content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT, default=0)
  commented = GenericForeignKey('commented_content_type', 'commented_object_id',)
