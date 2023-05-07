# Generated by Django 4.1.7 on 2023-04-30 09:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("attendance", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="attendance",
            name="status",
            field=models.CharField(
                choices=[
                    ("0", "Absent"),
                    ("1", "Present"),
                    ("2", "Late"),
                    ("3", "Excused"),
                ],
                max_length=1,
            ),
        ),
    ]