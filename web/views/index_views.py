import requests
from django.shortcuts import render, reverse, redirect
from django.views import generic
from web.models.user import User
from django.contrib.auth import login
from my_secrets.secrets import OSF_OAUTH_CLIENT_ID
from app.settings import OSF_REDIRECT_URI, OSF_CAS_URL, OSF_API_URL
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from web.utils import create_new_draft_registation, get_paginated_data


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


class WizardView(LoginRequiredMixin, generic.View):
    def get(self, request):
        schema = request.GET.get("schema")
        branched_from = request.GET.get("branched_from")
        if schema == 'open-ended':
            resp = create_new_draft_registation(OSF_API_URL, '5e13965879bee100010a790f', branched_from, request.user.token)
        elif schema == 'recipe':
            resp = create_new_draft_registation(OSF_API_URL, '5c252c8e0989e100220edb82', branched_from, request.user.token)
        draft_id = resp.json()['data']['id']

        return redirect(f'https://staging.osf.io/registries/drafts/{draft_id}')


class WizardIndex(LoginRequiredMixin, generic.TemplateView):
    template_name = "schema_wizard/wizard.html"
    login_url = reverse_lazy("osf_oauth")

    def get_context_data(self, **kwargs):
        """Insert the form into the context dict."""
        import asyncio
        kwargs.update({
            'nodes':  asyncio.run(get_paginated_data(self.request.user.token, f'{OSF_API_URL}v2/users/me/nodes/?fields[nodes]=title&page[size]=100'))
        })
        return super().get_context_data(**kwargs)
