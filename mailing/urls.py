from django.contrib import admin
from django.urls import path
from mailing import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.base, name='base'),
    path('clients/', views.ClientListView.as_view(), name='clients'),
    path('clients/add/', views.ClientCreateView.as_view(), name='client_add'),
    path('clients/<int:pk>/edit/', views.ClientUpdateView.as_view(), name='client_edit'),
    path('clients/<int:pk>/delete/', views.ClientDeleteView.as_view(), name='client_delete'),
    path('mailings/', views.MailingListView.as_view(), name='mailings'),
    path('mailings/add/', views.MailingCreateView.as_view(), name='mailing_add'),
    path('logs/', views.LogsView.as_view(), name='logs'),
    path('mailings/report/', views.MailingReportView.as_view(), name='mailing_report'),

]
