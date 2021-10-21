import json
from django.views.generic.edit import CreateView, DeleteView, UpdateView, FormView
from django.views.generic import TemplateView, View
from spam_scan.models import SpamUserData, UserProfileSpamReport
from django.shortcuts import reverse, redirect
from web.forms.schema_editor import SchemaForm, BlockForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class SpamScanView(LoginRequiredMixin, TemplateView):
    template_name = "spam_scan.html"
    login_url = reverse_lazy("osf_oauth")

    def get_context_data(self, *args, **kwargs):
        spam_user_data = SpamUserData.objects.exclude(
            social={}
        ).exclude(
            social__profileWebsites__0=None
        ).values('guid', 'full_name', 'social__profileWebsites').order_by('?').last()

        return {
            "potential_spammer": spam_user_data,
        }

    def post(self, *args, **kwargs):
        user = self.request.user
        score = self.request.POST['spam']
        if score == 'not-spam':
            score = 1
        elif score == 'dont-know':
            score = 2
        elif score == 'spam':
            score = 3
        else:
            raise NotImplementedError()

        UserProfileSpamReport.objects.update_or_create(
            user=user,
            user_spam_data=SpamUserData.objects.get(guid=self.request.POST['guid']),
            score=score
        )

        return redirect(reverse("spam_scan"))
