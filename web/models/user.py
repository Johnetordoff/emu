from django.contrib.auth.models import AbstractUser
from my_secrets.secrets import OSF_OAUTH_CLIENT_ID, OSF_OAUTH_SECRET_KEY
import urllib
import requests
from app import settings
from django.db import models
from web.fields import EncryptedTextField


class User(AbstractUser):
    guid = models.CharField(null=True, blank=True, max_length=500)
    refresh_token = models.CharField(null=True, blank=True, max_length=500)
    token = EncryptedTextField(null=True, blank=True, max_length=500)
    code = models.CharField(null=True, blank=True, max_length=500)
    admin = models.BooleanField(null=True, blank=True)
    bulk_contributors_csv = models.FileField(
        null=True, blank=True, upload_to="csv_uploads/bulk_contributors/"
    )

    def get_refresh_token(self):
        query_params = {
            "client_id": OSF_OAUTH_CLIENT_ID,
            "client_secret": OSF_OAUTH_SECRET_KEY,
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,

        }
        query_params = urllib.parse.urlencode(query_params)
        url = f"{settings.OSF_CAS_URL}oauth2/token?"
        url += query_params
        resp = requests.post(url)
        data = resp.json()
        token = data["access_token"]

        requests.get(
            settings.OSF_API_URL + "v2/", headers={"Authorization": f"Bearer {token}"}
        )
        self.save()

    @classmethod
    def from_osf_login(cls, code):
        query_params = {
            "redirect_uri": f"{settings.OSF_REDIRECT_URI}callback/",
            "client_id": OSF_OAUTH_CLIENT_ID,
            "client_secret": OSF_OAUTH_SECRET_KEY,
            "grant_type": "authorization_code",
            "access_type": "offline",
            "code": code,
        }
        query_params = urllib.parse.urlencode(query_params)
        url = f"{settings.OSF_CAS_URL}oauth2/token?"
        url += query_params
        resp = requests.post(url)
        data = resp.json()
        access_token = data["access_token"]
        refresh_token = data["refresh_token"]

        resp = requests.get(
            settings.OSF_API_URL + "v2/", headers={"Authorization": f"Bearer {access_token}"}
        )
        resp.raise_for_status()
        user_data = resp.json()

        fullname = user_data["meta"]["current_user"]["data"]["attributes"]["full_name"]
        guid = user_data["meta"]["current_user"]["data"]["id"]

        user, created = cls.objects.get_or_create(username=fullname)
        user.token = access_token
        user.guid = guid
        user.code = code
        user.refresh_token = refresh_token
        user.save()

        return user
