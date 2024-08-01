from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone


class Client(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    comment = models.TextField(blank=True)

    def __str__(self):
        return self.email

class Message(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()

    def __str__(self):
        return self.subject

class Mailing(models.Model):
    STATUS_CHOICES = (
        ('created', 'Created'),
        ('started', 'Started'),
        ('completed', 'Completed'),
    )
    date = models.DateTimeField()
    start_date = models.DateTimeField(default=timezone.now)
    frequency = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    message = models.OneToOneField(Message, on_delete=models.CASCADE)
    clients = models.ManyToManyField(Client)

    def __str__(self):
        return f"{self.date} - {self.status}"

    def send_mails(self):
        if self.status == 'created':
            subject = self.message.subject
            body = self.message.body
            clients = self.clients.all()
            for client in clients:
                send_mail(
                    subject,
                    body,
                    settings.EMAIL_HOST_USER,
                    [client.email],
                    fail_silently=False,
                )
            self.status = 'completed'
            self.save()
        else:
            raise ValueError("Mailing is not in 'created' status.")


class MailingAttempt(models.Model):
    STATUS_CHOICES = (
        ('successful', 'Successful'),
        ('failed', 'Failed'),
    )
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    response = models.TextField(blank=True)

    def __str__(self):
        return f"{self.mailing} - {self.status}"

class Log(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message[:50]
