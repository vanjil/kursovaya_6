from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Client, Mailing, Log
from .forms import MailingForm

class MailingReportView(ListView):
    model = Mailing
    template_name = 'mailing_report.html'
    context_object_name = 'mailings'

    def get_queryset(self):
        return Mailing.objects.filter(status='completed')

class LogsView(ListView):
    model = Log
    template_name = 'logs.html'
    context_object_name = 'logs'

class ClientListView(ListView):
    model = Client
    template_name = 'client_list.html'
    context_object_name = 'clients'

class ClientCreateView(CreateView):
    model = Client
    template_name = 'client_form.html'
    fields = ['email', 'name', 'comment']

class ClientUpdateView(UpdateView):
    model = Client
    template_name = 'client_form.html'
    fields = ['email', 'name', 'comment']

class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'client_confirm_delete.html'
    success_url = reverse_lazy('clients')

class MailingListView(ListView):
    model = Mailing
    template_name = 'mailing_list.html'
    context_object_name = 'mailings'

class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing_form.html'
    success_url = reverse_lazy('mailings')

    def form_valid(self, form):
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

def base(request):
    return render(request, 'base.html')
