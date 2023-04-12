from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from .models import *
from .utils import *
from .forms import *



class AthleteHome(DataMixin, ListView):
    model = Athlete
    template_name = 'athlete/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница')
        return context|c_def

    def get_queryset(self):
        return Athlete.objects.all().select_related('sport')


class ShowPost(DataMixin, DetailView):
    model = Athlete
    template_name = 'athlete/post.html'
    context_object_name = 'post'
    slug_url_kwarg = 'post_slug'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return context|c_def


class AthleteSports(DataMixin, ListView):
    model = Athlete
    template_name = 'athlete/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Athlete.objects.filter(sport__slug=self.kwargs['sport_slug']).select_related('sport')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        s = AthleteSport.objects.get(slug=self.kwargs['sport_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(s.name), sport_selected=s.pk)
        return context|c_def


def about(request):
    user_menu = menu.copy()
    if not request.user.is_authenticated:
        user_menu.pop(1)
    return render(request, 'athlete/about.html', {'menu': user_menu, 'title': 'О сайте'})


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'athlete/add_page.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('login')
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавить статью')
        return context|c_def


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'athlete/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Обратная связь')
        return context|c_def

    def form_valid(self, form):
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        message = form.cleaned_data['content']

        send_mail(
            f'Message from {name}',
            message,
            email,
            ['1vit77@rambler.ru'],
            fail_silently=False,
        )
        return super().form_valid(form)



class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'athlete/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return context|c_def

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'athlete/login.html'

    def get_success_url(self):
        return reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return context|c_def


def logout_user(request):
    logout(request)
    return redirect('login')