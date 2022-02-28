import csv
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
from django.utils import timezone


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
        ('given_name', 'Given Name'),
        ('family_name', 'Family Name'),
        ('middle_names', 'Middle Names'),
        ('_id', '_id'),
    )
    FIELDS_CHOICES = (
        ('_id', 'GUID'),
        ('full_name', 'Full Name'),
        ('given_name', 'Given Name'),
        ('family_name', 'Family Name'),
        ('middle_names', 'Middle Names'),
        ('_id', '_id'),
    )
    output = forms.ChoiceField(
        help_text='Select the format you want returned',
        required=True,
        choices=OUTPUT_CHOICES
    )
    filter_type = forms.ChoiceField(required=True, choices=FILTER_CHOICES)
    value = forms.CharField(required=True)
    fields = forms.MultipleChoiceField(
        help_text='Select one or more fields for output using the shift key',
        required=True,
        choices=FIELDS_CHOICES
    )


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
    login_url = reverse_lazy("osf_oauth")

    def post(self, *args, **kwargs):
        fields = dict(self.request.POST)['fields']
        value = self.request.POST['value']
        filter_type = self.request.POST['filter_type']
        output = self.request.POST['output']
        text = run(filter_search(filter=filter_type, value=value, fields=fields, output=output))
        if output == 'HTML':
            return render(request=self.request, context={'text': text, **self.get_context_data()}, template_name=self.template_name)
        elif output == 'CSV':

            response = HttpResponse(
                content_type='text/csv',
            )
            response['Content-Disposition'] = f'attachment; filename="{value}-{timezone.now()}.csv"'

            writer = csv.writer(response)
            writer.writerows(text)
            return response
