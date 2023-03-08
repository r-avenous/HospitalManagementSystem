# Generated by Django 4.1.7 on 2023-03-08 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hospital", "0034_remove_patient_email"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="room",
            name="available",
        ),
        migrations.AddField(
            model_name="room",
            name="cost",
            field=models.PositiveIntegerField(default=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="room",
            name="max_capacity",
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name="room",
            name="occupied_capacity",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
