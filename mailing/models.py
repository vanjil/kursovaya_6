from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
import smtplib
from django.contrib.auth.models import AbstractUser


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    views = models.PositiveIntegerField(default=0)
    publication_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username


class Client(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    comment = models.TextField(blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.email

class Message(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.subject

class Mailing(models.Model):
    STATUS_CHOICES = (
        ('created', 'Created'),
        ('started', 'Started'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )
    date = models.DateTimeField()
    start_date = models.DateTimeField(default=timezone.now)
    frequency = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='created')
    message = models.OneToOneField(Message, on_delete=models.CASCADE)
    clients = models.ManyToManyField(Client)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return f"{self.date} - {self.status}"

    def send_mails(self):
        if self.status == 'created':
            subject = self.message.subject
            body = self.message.body
            clients = self.clients.all()
            try:
                server_response = send_mail(
                    subject,
                    body,
                    settings.EMAIL_HOST_USER,
                    [client.email for client in clients],
                    fail_silently=False,
                )
                MailingAttempt.objects.create(
                    mailing=self,
                    status='successful',
                    response=f"Sent {server_response} messages"
                )
                self.status = 'completed'
            except smtplib.SMTPException as e:
                MailingAttempt.objects.create(
                    mailing=self,
                    status='failed',
                    response=str(e)
                )
                self.status = 'failed'
            self.save()
        else:
            raise ValueError("Mailing is not in 'created' status.")

class MailingAttempt(models.Model):
    STATUS_CHOICES = (
        ('successful', 'Successful'),
        ('failed', 'Failed'),
    )
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='attempts')
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
