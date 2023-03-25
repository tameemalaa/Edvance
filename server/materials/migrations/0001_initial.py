# Generated by Django 4.1.7 on 2023-03-25 05:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("courses", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Material",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("link", models.CharField(max_length=255)),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("0", "lecture slides"),
                            ("1", "reading"),
                            ("2", "video lecture"),
                            ("3", "other"),
                        ],
                        max_length=1,
                    ),
                ),
                (
                    "course",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="courses.course",
                    ),
                ),
                (
                    "section",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="courses.section",
                    ),
                ),
            ],
        ),
    ]
