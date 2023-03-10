# Generated by Django 4.1.7 on 2023-03-10 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hospital", "0036_patient_email"),
    ]

    operations = [
        migrations.AlterField(
            model_name="admin",
            name="mobile",
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="dataentryoperator",
            name="mobile",
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="patient",
            name="mobile",
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name="patientdischargedetails",
            name="mobile",
            field=models.IntegerField(null=True),
        ),
    ]