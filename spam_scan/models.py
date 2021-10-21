from django.db import models
from web.models.user import User


class SpamUserData(models.Model):
    guid = models.CharField(max_length=500, blank=True, null=True, unique=True)
    full_name = models.CharField(max_length=500, blank=True, null=True)
    social = models.JSONField(blank=True, null=True)
    education = models.JSONField(blank=True, null=True)
    employment = models.JSONField(blank=True, null=True)


class SpamRegistrationData(models.Model):
    guid = models.CharField(max_length=500, blank=True, null=True, unique=True)
    title = models.CharField(max_length=500, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    raw_json = models.JSONField(blank=True, null=True)
    spam_reports = models.ManyToManyField(User, through="SpamReport")


class SpamReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    registration = models.ForeignKey(SpamRegistrationData, on_delete=models.CASCADE)
    notes = models.TextField(blank=True, null=True)
    score = models.PositiveIntegerField(blank=True, null=True)


class UserProfileSpamReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_spam_data = models.ForeignKey(SpamUserData, on_delete=models.CASCADE)
    notes = models.TextField(blank=True, null=True)
    score = models.PositiveIntegerField(blank=True, null=True)
