from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import FormView, FormMixin

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login

from django.views.generic.base import View
from django.contrib.auth import logout

from django.views.generic import ListView, DetailView
from .models import Photo, Like, Comment
from django.http import JsonResponse

from django.core.exceptions import ObjectDoesNotExist

from django.urls import reverse
from django.contrib.contenttypes.models import ContentType





class CreateLikeView(FormView):

  def post(self, request, photo_id, *args, **kwargs):
    if request.user.is_authenticated:
      like = Like(user_id=request.user.id, photo_id=photo_id)
      like.save()
      likes_count = Like.objects.all().filter(photo_id=photo_id).count()
      return JsonResponse({"likes_count": likes_count}, status=200)
    else:
      return JsonResponse({}, status=401)



class DeleteLikeView(FormView):

  def post(self, request, photo_id, *args, **kwargs):
    if request.user.is_authenticated:
      like = Like.objects.get(user_id=request.user.id, photo_id=photo_id)
      like.delete()
      likes_count = Like.objects.all().filter(photo_id=photo_id).count()

      return JsonResponse({"likes_count": likes_count}, status=200)
    else:
      return JsonResponse({}, status=401)



class PhotosListView(ListView):
  model = Photo
  paginate_by = 8

  def get_queryset(self):
    field = self.request.GET.get('order')
    list_photos = Photo.objects.all() if field is None else Photo.objects.all().order_by(field)
    return list_photos

  def get_context_data(self, **kwargs):
    context = super(PhotosListView, self).get_context_data(**kwargs)
    order = self.request.GET.get('order')
    context['order'] = order
    return context

class PhotoShowView(FormMixin, DetailView):
  model = Photo
  pk_url_kwarg = 'photo_id'
  form_class = CommentForm

  def get_success_url(self):
    return reverse('show_photo', args=[str(self.object.id)])

  def post(self, request, photo_id, *args, **kwargs):
    self.object = self.get_object()
    form = self.get_form()
    if form.is_valid():
      comment = Comment(commented=self.object, user=request.user, text=request.POST.get('text'))
      comment.save()
      return self.form_valid(form)
    else:
      return self.form_invalid(form)

  def get(self, request, photo_id, *args, **kwargs):
    photo = Photo.objects.get(id=photo_id)
    try:
      photo.like_set.get(user_id=request.user.id)
      current_user_like_photo = True
    except ObjectDoesNotExist:
      current_user_like_photo = False
    comment_list = Comment.objects.filter(commented_object_id=photo.id, commented_content_type=ContentType.objects.get_for_model(Photo))
    context = {'current_user_like_photo': current_user_like_photo, 'photo': photo, 'form': self.get_form(), 'comment_list': comment_list}
    return render(request, 'contest/photo_detail.html', context)


class RegisterFormView(FormView):
  form_class = UserRegisterForm
  success_url = "/login/"
  template_name = "register.html"

  def form_valid(self, form):
    form.save()
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
      photo = Photo(title=form.cleaned_data['title'], image=form.cleaned_data['image'],  author = request.user)
      photo.save()
      return redirect('home')
  return render(request, 'new_photo_form.html', {'form': form})

