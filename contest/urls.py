from django.urls import path
from django.conf.urls import url
from django.views.generic.base import RedirectView
from django.urls import include
from django.contrib.auth import logout
from django.conf import settings


from . import views

urlpatterns = [
  url(r'^register$', views.RegisterFormView.as_view(), name='registration'),
  url(r'^login/$', views.LoginFormView.as_view(), name='login'),
  url(r'^logout$', views.LogoutFormView.as_view(), name='logout'),
  url(r'^photos/new/$', views.upload_photo, name='new_photo'),
  #path('image_upload', views.hotel_image_view, name = 'image_upload'),
  #path('success', views.success, name = 'success'),
  url(r'^photos/$', views.PhotosListView.as_view(), name='list_photos'),
  url(r'^photos/(?P<photo_id>\d+)$', views.PhotoShowView.as_view(), name='show_photo'),
  url(r'^photos/(?P<photo_id>\d+)/create_like/$', views.CreateLikeView.as_view(), name='add_like'),
  url(r'^photos/(?P<photo_id>\d+)/delete_like/$', views.DeleteLikeView.as_view(), name='delete_like'),
  path('', RedirectView.as_view(url='photos/'), name='home'),
  path('', include('social_django.urls', namespace='social')),
  #path('logout/', logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
]

