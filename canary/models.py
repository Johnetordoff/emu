from django.db import models

from web.models import User


class SpamReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='spam_reports')
    url = models.CharField(max_length=5000)
