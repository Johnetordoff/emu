import json
from django import forms

from django.views.generic import TemplateView
from web.models import Block
from django.views.generic.edit import FormView
from django.forms import ModelForm
from canary.models import SpamReport
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


class SpamReportForm(ModelForm):
    url = forms.URLField(max_length=500000, required=True)

    class Meta:
        model = SpamReport
        fields = ["url"]


class SpamReportCSVForm(ModelForm):
    csv = forms.URLField(max_length=500000, required=True)

    class Meta:
        model = SpamReport
        fields = ["url"]


class ReportSpamListView(LoginRequiredMixin, TemplateView, FormView):
    pass


class ReportSpamView(LoginRequiredMixin, TemplateView, FormView):
    template_name = "canary/report_spam.html"
    form_class = SpamReportForm
    success_url = reverse_lazy('report_spam')

    def post(self, *args, **kwargs):
        SpamReport.create(
            url=self.request.POST['url'],
            user=self.request.user,
        )
        return super().post(self, *args, **kwargs)
