from django.contrib import admin
from django.urls import path
from .views import (
    ClientListView, ClientCreateView, ClientUpdateView, ClientDeleteView,
    MailingListView, MailingCreateView, MailingUpdateView, MailingDeleteView,
    MailingReportView, LogsView, HomePageView, blog_view
)

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('clients/', ClientListView.as_view(), name='clients'),
    path('clients/create/', ClientCreateView.as_view(), name='client_create'),
    path('clients/<int:pk>/edit/', ClientUpdateView.as_view(), name='client_update'),
    path('clients/<int:pk>/delete/', ClientDeleteView.as_view(), name='client_delete'),

    path('mailings/', MailingListView.as_view(), name='mailings'),
    path('mailings/create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailings/<int:pk>/edit/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailings/<int:pk>/delete/', MailingDeleteView.as_view(), name='mailing_delete'),

    path('logs/', LogsView.as_view(), name='logs'),
    path('mailing_report/', MailingReportView.as_view(), name='mailing_report'),
    path('blog/', blog_view, name='blog'),
]
