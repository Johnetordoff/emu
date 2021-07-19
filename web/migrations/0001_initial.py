# Generated by Django 3.1.1 on 2021-06-20 18:12

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, verbose_name="email address"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                ("token", models.CharField(blank=True, max_length=500, null=True)),
                ("admin", models.BooleanField(blank=True, null=True)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.Group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.Permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Schema",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=500, null=True)),
                ("version", models.PositiveIntegerField()),
                (
                    "description",
                    models.CharField(blank=True, max_length=5000, null=True),
                ),
                ("csv_uploads", models.FileField(blank=True, null=True, upload_to="")),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="schemas",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Block",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nav", models.CharField(blank=True, max_length=5000, null=True)),
                (
                    "help_text",
                    models.CharField(
                        blank=True, help_text="AKA help", max_length=5000, null=True
                    ),
                ),
                (
                    "display_text",
                    models.CharField(
                        blank=True, help_text="AKA title", max_length=5000, null=True
                    ),
                ),
                (
                    "example_text",
                    models.CharField(
                        blank=True, help_text="AKA example", max_length=5000, null=True
                    ),
                ),
                (
                    "block_type",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("page-heading", "Page Heading"),
                            ("section-heading", "Section Heading"),
                            ("subsection-heading", "Subsection Heading"),
                            ("paragraph", "Paragraph"),
                            ("question-label", "Question Label"),
                            ("short-text-input", "Short Text Input"),
                            ("long-text-input", "Long Text Input"),
                            ("file-input", "File Input"),
                            ("contributors-input", "Contributors Input"),
                            ("single-select-input", "Single Select Input"),
                            ("multi-select-input", "Multi-select Input"),
                            ("select-input-option", "Select Input Option"),
                            ("select-other-option", "Select Other Option"),
                        ],
                        max_length=50000,
                        null=True,
                    ),
                ),
                (
                    "options",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=100),
                        blank=True,
                        help_text="Enter as comma separated list",
                        null=True,
                        size=None,
                    ),
                ),
                ("required", models.BooleanField(null=True)),
                ("index", models.PositiveIntegerField(blank=True, null=True)),
                (
                    "schema",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="blocks",
                        to="web.schema",
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="block",
            constraint=models.CheckConstraint(
                check=models.Q(
                    models.Q(_negated=True, block_type="page-heading"),
                    models.Q(
                        ("example_text__isnull", True),
                        ("block_type", "page-heading"),
                        ("help_text__isnull", True),
                    ),
                    _connector="OR",
                ),
                name="check_page_heading",
            ),
        ),
        migrations.AddConstraint(
            model_name="block",
            constraint=models.CheckConstraint(
                check=models.Q(
                    models.Q(_negated=True, block_type="section-heading"),
                    models.Q(
                        ("example_text__isnull", True),
                        ("block_type", "section-heading"),
                        ("help_text__isnull", True),
                    ),
                    _connector="OR",
                ),
                name="check_section_heading",
            ),
        ),
        migrations.AddConstraint(
            model_name="block",
            constraint=models.CheckConstraint(
                check=models.Q(
                    models.Q(_negated=True, block_type="file-input"),
                    models.Q(
                        ("display_text__isnull", True),
                        ("example_text__isnull", True),
                        ("block_type", "file-input"),
                        ("help_text__isnull", True),
                    ),
                    _connector="OR",
                ),
                name="check_file_input",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="block",
            unique_together={("schema", "index")},
        ),
    ]
