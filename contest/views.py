from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import FormView

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login

from django.views.generic.base import View
from django.contrib.auth import logout

from django.views.generic import ListView, DetailView
from .models import Photo, Like
from django.http import JsonResponse

from django.core.exceptions import ObjectDoesNotExist



class CreateLikeView(FormView):

  def post(self, request, photo_id, *args, **kwargs):
    like = Like(user_id=request.user.id, photo_id=photo_id)
    like.save()
    likes_count = Like.objects.all().filter(photo_id=photo_id).count()

    return JsonResponse({"likes_count": likes_count}, status=200)



class DeleteLikeView(FormView):

  def post(self, request, photo_id, *args, **kwargs):
    like = Like.objects.get(user_id=request.user.id, photo_id=photo_id)
    like.delete()
    likes_count = Like.objects.all().filter(photo_id=photo_id).count()

    return JsonResponse({"likes_count": likes_count}, status=200)




class PhotosListView(ListView):
  model = Photo

  def get_queryset(self):

    return Photo.objects.all()




class PhotoShowView(DetailView):
  model = Photo
  pk_url_kwarg = 'photo_id'

  def get(self, request, photo_id, *args, **kwargs):
    photo = Photo.objects.get(id=photo_id)
    try:
      photo.like_set.get(user_id=request.user.id)
      current_user_like_photo = True
    except ObjectDoesNotExist:
      current_user_like_photo = False
    context = {'current_user_like_photo': current_user_like_photo, 'photo': photo}

    return render(request, 'contest/photo_detail.html', context)

  def get_context_data(self, **kargs):
    context = super(PhotoShowView, self).get_context_data(**kargs)
    context['flager'] = 'sdsds'

    return context

class RegisterFormView(FormView):
  # Указажем какую форму мы будем использовать для регистрации наших пользователей, в нашем случае
  # это UserCreationForm - стандартный класс Django унаследованный
  form_class = UserRegisterForm

  # Ссылка, на которую будет перенаправляться пользователь в случае успешной регистрации.
  # В данном случае указана ссылка на страницу входа для зарегистрированных пользователей.
  success_url = "/login/"

  # Шаблон, который будет использоваться при отображении представления.
  template_name = "register.html"

  def form_valid(self, form):
    form.save()
        # Функция super( тип [ , объект или тип ] )
        # Возвратите объект прокси, который делегирует вызовы метода родительскому или родственному классу типа .
    return super(RegisterFormView, self).form_valid(form)

  def form_invalid(self, form):
    return super(RegisterFormView, self).form_invalid(form)

class LoginFormView(FormView):
  form_class = AuthenticationForm

  success_url = '/'

  template_name = 'login.html'

  def form_valid(self, form):
    self.user = form.get_user()
    login(self.request, self.user)
    return super(LoginFormView, self).form_valid(form)


class LogoutFormView(FormView):
  def get(self, request):
    logout(request)

    return redirect('home')



def upload_photo(request):
  form = PhotoUploadForm()
  if request.method == 'POST':
    form = PhotoUploadForm(request.POST, request.FILES)
    if form.is_valid():
      photo = form.save()
      photo.author = request.user
      photo.save()
      return redirect('home')
  return render(request, 'new_photo_form.html', {'form': form})


def index(request):
  return render(request, 'index.html')
