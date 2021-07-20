from django.shortcuts import render, reverse, redirect
from django.views import generic
from web.models.user import User
from django.contrib.auth import login
from my_secrets.secrets import OSF_OAUTH_CLIENT_ID
from app.settings import OSF_REDIRECT_URI, OSF_CAS_URL


def index(request):
    return render(request, "index.html")


class OSFOauthView(generic.TemplateView):
    def get(self, request):
        return redirect(
            f"{OSF_CAS_URL}oauth2/authorize/?client_id={OSF_OAUTH_CLIENT_ID}"
            f"&redirect_uri={OSF_REDIRECT_URI}callback/"
            f"&scope=osf.full_write"
            f"&response_type=code"
        )


class OSFOauthCallbackView(generic.View):
    def get(self, request):
        code = request.GET.get("code")
        state = request.GET.get("state")
        user = User.from_osf_login(code)
        user.save()
        login(request, user)
        return redirect(reverse("home"))
