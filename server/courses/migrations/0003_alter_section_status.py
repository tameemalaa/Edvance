# Generated by Django 4.1.7 on 2023-04-30 08:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0002_alter_course_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="section",
            name="status",
            field=models.CharField(
                choices=[("0", "Past"), ("1", "Present"), ("2", "Future")], max_length=1
            ),
        ),
    ]
