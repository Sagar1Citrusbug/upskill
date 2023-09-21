# Generated by Django 4.2.5 on 2023-09-21 11:05

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Company",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "created_by",
                    models.EmailField(blank=True, max_length=254, null=True),
                ),
                (
                    "updated_by",
                    models.EmailField(blank=True, max_length=254, null=True),
                ),
                ("is_active", models.BooleanField(default=True)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=100)),
            ],
            options={
                "verbose_name": "Company",
                "verbose_name_plural": "Companies",
                "db_table": "company",
            },
        ),
    ]
