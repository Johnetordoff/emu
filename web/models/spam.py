from django.contrib.auth.models import AbstractUser
from my_secrets.secrets import OSF_OAUTH_CLIENT_ID, OSF_OAUTH_SECRET_KEY
import urllib
import requests
from app import settings
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.shortcuts import render, reverse, redirect, HttpResponse
from django.db.models import CheckConstraint, Q, F, Case
from django.contrib.postgres.fields.jsonb import JSONField
from web.models.user import User

class SpamUserData(models.Model):
    guid = models.CharField(max_length=500, blank=True, null=True, unique=True)
    full_name = models.CharField(max_length=500, blank=True, null=True)
    social = JSONField(blank=True, null=True)
    education = JSONField(blank=True, null=True)
    employment = JSONField(blank=True, null=True)


class SpamRegistrationData(models.Model):
    guid = models.CharField(max_length=500, blank=True, null=True, unique=True)
    title = models.CharField(max_length=500, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    raw_json = JSONField(blank=True, null=True)
    spam_reports = models.ManyToManyField(User, through='SpamReport')


class SpamReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    registration = models.ForeignKey(SpamRegistrationData, on_delete=models.CASCADE)
    notes = models.TextField(blank=True, null=True)
    score = models.PositiveIntegerField(max_length=5, blank=True, null=True)
