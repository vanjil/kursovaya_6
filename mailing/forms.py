from django import forms
from .models import Client, Mailing, Message
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Mailing


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['email', 'name', 'comment']

class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['start_date', 'frequency', 'status', 'message', 'clients']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['clients'].widget = forms.CheckboxSelectMultiple()
        self.fields['message'].queryset = Message.objects.all()

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }

class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing_form.html'
    success_url = reverse_lazy('mailings')
