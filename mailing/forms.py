from django import forms
from .models import Client, Mailing, Message
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['email', 'name', 'comment']

class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['start_date', 'frequency', 'status', 'message', 'clients']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['clients'].widget = forms.CheckboxSelectMultiple()
        if user:
            self.fields['message'].queryset = Message.objects.filter(owner=user)
            self.fields['clients'].widget = forms.CheckboxSelectMultiple()


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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
