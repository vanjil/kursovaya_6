from django.contrib import admin
from .models import Client, Message, Mailing, MailingAttempt

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'comment')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'body')

@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'frequency', 'status', 'message')
    filter_horizontal = ('clients',)
    actions = ['send_selected_mailings']

    def send_selected_mailings(self, request, queryset):
        for mailing in queryset:
            try:
                mailing.send_mails()
                self.message_user(request, f"Mailing {mailing.id} sent successfully.")
            except Exception as e:
                self.message_user(request, f"Error sending mailing {mailing.id}: {str(e)}", level='error')

    send_selected_mailings.short_description = "Send selected mailings"

@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ('mailing', 'date', 'status', 'response')
