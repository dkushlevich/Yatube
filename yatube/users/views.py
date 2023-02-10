from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, TemplateView
from users.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.contrib.auth import authenticate, login

from users.forms import CreationForm, UserProfileForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('users:intro')
    template_name = 'users/signup.html'

    def form_valid(self, form):
        valid = super(SignUp, self).form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        new_user = authenticate(username=username, password=password)
        login(self.request, new_user)
        return valid


class UserProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'users/profile.html'
    form_class = UserProfileForm
    model = User

    def get_success_url(self):
        return reverse('users:profile', kwargs={'pk': self.request.user.id})

    def get_object(self, queryset=None):
        return self.request.user

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        print(obj)
        if obj != self.request.user:
            raise Http404("You are not allowed to edit this Post")
        return super(UserProfileView, self).dispatch(request, *args, **kwargs)


class IntroView(TemplateView):
    template_name = 'users/intro.html'
