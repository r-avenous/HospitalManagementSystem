# Generated by Django 4.1.7 on 2023-03-10 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hospital", "0037_alter_admin_mobile_alter_dataentryoperator_mobile_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="doctor",
            name="mobile",
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="frontdeskoperator",
            name="mobile",
            field=models.IntegerField(null=True),
        ),
    ]
