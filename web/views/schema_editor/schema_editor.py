import csv
import codecs

from django.views.generic.edit import CreateView, DeleteView, UpdateView, FormView
from django.views.generic import TemplateView, View
from web.models import Schema, Block
from django.shortcuts import reverse, redirect
from web.forms.schema_editor import SchemaForm, BlockForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http.response import JsonResponse
from django.contrib import messages
from django.db.utils import IntegrityError
from django.forms.fields import HiddenInput


class SchemaCreateView(LoginRequiredMixin, CreateView):
    model = Schema
    fields = ["name", "version"]

    def post(self, request, *args, **kwargs):
        form = SchemaForm(request.POST)

        if form.is_valid():
            schema = form.save()
            schema.user = request.user
            schema.save()
        else:
            raise Exception(form.__dict__)
        return redirect(reverse("schema_editor"))


class CSVtoSchemaView(LoginRequiredMixin, View):

    def get_context_data(self, *args, **kwargs):
        form = SchemaForm(self.request.GET, self.request.FILES)

        return {
            "form": form,
        }

    def post(self, request, *args, **kwargs):
        form = SchemaForm(request.POST, request.FILES)
        if form.is_valid():
            csv = form.files["csv"]
            user = request.user
            user.csv = csv
            user.save()
            if csv:
                schema = self.read_csv(csv, request)

        return redirect(
            reverse("block_editor", kwargs={"schema_id": schema.id })
        )

    def read_csv(self, file, request):
        user = request.user

        schema = Schema(name='Untitled', version=0, user=user)
        schema.save()

        for row in csv.DictReader(codecs.iterdecode(file.file, "utf-8"), delimiter=","):
            row["required"] = True if row.pop("required") == "TRUE" else False
            block = Block(**row)
            block.schema_id = schema.id
            block.user = request.user
            block.save()
            block.index = block.schema.blocks.count() + 1
            block.save()

        return schema


class BlockEditorView(TemplateView, FormView):
    template_name = "schema_editor/block_editor.html"
    form_class = BlockForm

    def get_context_data(self, *args, **kwargs):
        schema = Schema.objects.get(id=self.kwargs["schema_id"])

        form = SchemaForm(self.request.GET, self.request.FILES)

        return {
            "form": form,
            "schema": schema,
            "blocks": Block.objects.filter(
                schema__user=self.request.user, schema_id=self.kwargs["schema_id"]
            ).order_by("index"),
            "block_types": [block_type[0] for block_type in Block.SCHEMABLOCKS],
        }


    def get_success_url(self):
        return reverse(
            "block_editor",
            kwargs={"schema_id": Block.get(id=self.kwargs["block"]).schema.id},
        )


class SchemaJSONView(View):
    def get(self, request, schema_id):
        return JsonResponse(Schema.objects.get(id=schema_id).to_json)


class SimpleSchemaJSONView(View):
    def get(self, request, schema_id):
        return JsonResponse(Schema.objects.get(id=schema_id).to_atomic_schema)


class SchemaUpdateView(LoginRequiredMixin, UpdateView):
    pk_url_kwarg = "schema_id"

    model = Schema

    def post(self, request, *args, **kwargs):
        form = SchemaForm(request.POST, request.FILES)
        if form.is_valid():
            Schema.objects.filter(id=self.kwargs["schema_id"]).update(
                **form.cleaned_data
            )
            csv = request.FILES.get("csv_uploads")
            schema = Schema.objects.get(id=self.kwargs["schema_id"])
            schema.csv = csv
            schema.save()
            if csv:
                self.read_csv(schema.csv)
        else:
            raise Exception(form.__dict__)
        return redirect(
            reverse("block_editor", kwargs={"schema_id": self.kwargs["schema_id"]})
        )

    def read_csv(self, file):
        import csv

        with open(file.name, "r") as fp:
            spamreader = csv.reader(fp, delimiter=",")
            for row in spamreader:
                print(row)
                data = row[0]


class SchemaDeleteView(LoginRequiredMixin, DeleteView):
    model = Schema
    success_url = reverse_lazy("schema_editor")
    pk_url_kwarg = "schema_id"


class BlockCreateView(LoginRequiredMixin, CreateView):
    model = Block
    fields = ["display_text", "block_type"]

    def post(self, request, *args, **kwargs):
        form = BlockForm(request.POST)
        if form.is_valid():
            form.cleaned_data.pop('csv')
            block = Block(**form.cleaned_data)
            block.schema_id = self.kwargs["schema_id"]
            block.user = request.user
            block.save()
            block.index = block.schema.blocks.count() + 1
            block.save()
        else:
            raise Exception(form.__dict__)
        return redirect(
            reverse("block_editor", kwargs={"schema_id": self.kwargs["schema_id"]})
        )


class BlockUpdateView(LoginRequiredMixin, UpdateView, FormView):
    model = Block
    success_url = reverse_lazy("block_editor")
    pk_url_kwarg = "block_id"
    template_name = "schema_editor/change_block.html"
    form_class = BlockForm

    def get_context_data(self, *args, **kwargs):
        block = self.get_object()
        form = self.form_class(
            initial={
                "display_text": block.display_text,
                "block_type": block.block_type,
                "required": block.required,
                "index": block.index,
            }
        )
        form.display_text = self.get_object().display_text
        form.block_type = self.get_object().block_type
        form.fields['csv'].widget = HiddenInput()

        return {
            "block_id": self.kwargs["block_id"],
            "schema_id": self.kwargs["schema_id"],
            "form": form,
        }

    def form_valid(self, form):
        """If the form is valid, save the associated model."""

        try:
            self.object = form.save()
        except IntegrityError as e:
            if 'duplicate key value violates unique constraint' in e.args[0]:
                blocking_block = Block.objects.get(index=self.object.index, schema_id=self.kwargs['schema_id'])
                url = reverse("block-update", kwargs={
                    "schema_id": self.kwargs["schema_id"],
                    "block_id": blocking_block.id
                })
                messages.add_message(self.request, messages.ERROR, f'Index `{self.object.index}'
                                                                   f' already used by <a href={url}>{blocking_block}</a>',
                                     extra_tags='safe')
                return redirect(
                    reverse("block-update", kwargs={
                        "schema_id": self.kwargs["schema_id"],
                        "block_id": self.kwargs["block_id"]
                    })
                )

        return super().form_valid(form)


    def get_success_url(self):
        return reverse("block_editor", kwargs={"schema_id": self.kwargs["schema_id"]})


class BlockDeleteView(LoginRequiredMixin, DeleteView):
    model = Block
    pk_url_kwarg = "block_id"

    def get_success_url(self):
        return reverse("block_editor", kwargs={"schema_id": self.kwargs["schema_id"]})


class SchemaEditorView(LoginRequiredMixin, TemplateView, FormView):
    template_name = "schema_editor/schema_editor.html"
    form_class = SchemaForm
    login_url = reverse_lazy("osf_oauth")

    def get_context_data(self, *args, **kwargs):
        return {"schemas": Schema.objects.all()}

    def get_success_url(self):
        return reverse("schema_editor")
