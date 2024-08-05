from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Log
from .forms import MailingForm
from .models import Mailing, Client

from django.views.generic import TemplateView
from django.views.decorators.cache import cache_page

from django.views.generic import ListView
from .models import BlogPost

class BlogListView(ListView):
    model = BlogPost
    template_name = 'home.html'
    context_object_name = 'posts'

def blog_view(request):
    posts = BlogPost.objects.all()
    return render(request, 'blog.html', {'posts': posts})

@cache_page(60 * 15)  # Кешировать на 15 минут
class HomePageView(TemplateView):
    template_name = 'home.html'

class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Данные для главной страницы
        total_mailings = Mailing.objects.count()
        active_mailings = Mailing.objects.filter(status='active').count()
        unique_clients = Client.objects.distinct().count()

        # Получение трех случайных статей
        recent_blog_posts = BlogPost.objects.order_by('-publication_date')[:3]

        context.update({
            'total_mailings': total_mailings,
            'active_mailings': active_mailings,
            'unique_clients': unique_clients,
            'random_blogs': recent_blog_posts
        })
        return context


class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_mailings'] = Mailing.objects.count()
        context['active_mailings'] = Mailing.objects.filter(status='active').count()
        context['unique_clients'] = Client.objects.distinct().count()
        context['random_blogs'] = Blog.objects.order_by('?')[:3]
        return context


class MailingReportView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'mailing_report.html'
    context_object_name = 'mailings'

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user, status='completed')

class LogsView(LoginRequiredMixin, ListView):
    model = Log
    template_name = 'logs.html'
    context_object_name = 'logs'

class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'client_list.html'
    context_object_name = 'clients'

    def get_queryset(self):
        return Client.objects.filter(owner=self.request.user)

class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    template_name = 'client_form.html'
    fields = ['email', 'name', 'comment']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    template_name = 'client_form.html'
    fields = ['email', 'name', 'comment']

    def get_queryset(self):
        return Client.objects.filter(owner=self.request.user)

class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    template_name = 'client_confirm_delete.html'
    success_url = reverse_lazy('clients')

    def get_queryset(self):
        return Client.objects.filter(owner=self.request.user)

class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'mailing_list.html'
    context_object_name = 'mailings'

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)

class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing_form.html'
    success_url = reverse_lazy('mailings')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        mailing = form.instance
        self.send_mailing(mailing)
        return response

    def send_mailing(self, mailing):
        subject = mailing.message.subject
        body = mailing.message.body
        clients = mailing.clients.all()

        for client in clients:
            send_mail(
                subject,
                body,
                'vanjilbrooklyn@gmail.com',
                [client.email],
                fail_silently=False,
            )

        mailing.status = 'completed'
        mailing.save()

class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing_form.html'
    success_url = reverse_lazy('mailings')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = 'mailing_confirm_delete.html'
    success_url = reverse_lazy('mailings')

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)

def base(request):
    return render(request, 'base.html')
