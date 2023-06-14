import logging
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from main.forms import RegisterForm, LoginForm
from main.utils import DataMixin

logger = logging.getLogger(__name__)


def index(request):
    return render(request, "index.html")


class Register(DataMixin, CreateView):
    form_class = RegisterForm
    template_name = 'auth/register.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        utils_context = self.get_context(title='Registration')
        return dict(list(context.items()) + list(utils_context.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)

        logger.info(f'{self.request.user} registered')

        return redirect('home')


class Login(DataMixin, LoginView):
    form_class = LoginForm
    template_name = 'auth/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        u_context = self.get_context(title="Authorization")
        return dict(list(context.items()) + list(u_context.items()))

    def get_success_url(self):
        logger.info(f'{self.request.user} logged in')

        return reverse_lazy('home')


def user_logout(request):
    logger.info(f'{request.user} logged out')

    logout(request)
    return redirect('home')


class Profile(DataMixin, TemplateView):
    template_name = 'profile/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        u_context = self.get_context(title="Profile")
        return dict(list(context.items()) + list(u_context.items()))

