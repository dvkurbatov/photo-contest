from django.contrib import admin

from .models import Photo, Like, Comment

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
  list_display = ('title', 'image_tag', 'author', 'likes_count', 'created_at')
  search_fields = ['title']
  fields = ('title', 'author', 'image_tag', 'created_at',)
  readonly_fields = ('image_tag', 'created_at')
