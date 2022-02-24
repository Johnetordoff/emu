import csv
import requests
from django import forms

from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.forms import ModelForm
from canary.models import SpamReport
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from canary.management.commands.filter_search import filter_search
from django.shortcuts import render
from asyncio import run
from django.http import HttpResponse


class SpamReportForm(ModelForm):
    url = forms.URLField(max_length=500000, required=True)

    class Meta:
        model = SpamReport
        fields = ["url"]


class UserFilterSearch(forms.Form):

    OUTPUT_CHOICES = (
        ('HTML', 'html'),
        ('CSV', 'csv'),
    )
    FILTER_CHOICES = (
        ('full_name', 'Full Name'),
    )
    FIELDS_CHOICES = (
        ('_id', 'GUID'),
        ('full_name', 'Full Name'),
    )
    output = forms.ChoiceField(
        required=True,
        choices=OUTPUT_CHOICES
    )
    filter_type = forms.ChoiceField(required=True, choices=FILTER_CHOICES)
    value = forms.CharField(required=True)
    fields = forms.MultipleChoiceField(required=True, choices=FIELDS_CHOICES)


class ReportSpamListView(LoginRequiredMixin, TemplateView, FormView):
    pass


class ReportSpamView(LoginRequiredMixin, TemplateView, FormView):
    template_name = "canary/report_spam.html"
    form_class = UserFilterSearch
    success_url = reverse_lazy('report_spam')

    def post(self, *args, **kwargs):
        SpamReport.create(
            url=self.request.POST['url'],
            user=self.request.user,
        )
        return super().post(self, *args, **kwargs)


class UserQuickSearch(LoginRequiredMixin, TemplateView, FormView):
    template_name = "canary/report_spam.html"
    form_class = UserFilterSearch
    success_url = reverse_lazy('report_spam')

    def post(self, *args, **kwargs):
        fields = dict(self.request.POST)['fields']
        value = self.request.POST['value']
        filter_type = self.request.POST['filter_type']
        output = self.request.POST['output']
        print(output)
        text = run(filter_search(filter=filter_type, value=value, fields=fields, output=output))
        print(text)
        if output == 'html':
            return render(request=self.request, context={'text': text}, template_name=self.template_name)
        elif output == 'CSV':
            response = HttpResponse(
                content_type='text/csv',
            )
            print(response)
            print(response)
            writer = csv.writer(response)
            writer.writerows(text)
            print(text)
            return response
