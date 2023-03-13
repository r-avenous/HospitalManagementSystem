# Generated by Django 4.1.7 on 2023-03-11 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hospital", "0038_alter_doctor_mobile_alter_frontdeskoperator_mobile"),
    ]

    operations = [
        migrations.AlterField(
            model_name="admin",
            name="mobile",
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="dataentryoperator",
            name="mobile",
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="doctor",
            name="mobile",
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="frontdeskoperator",
            name="mobile",
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="patient",
            name="mobile",
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name="patientdischargedetails",
            name="mobile",
            field=models.CharField(max_length=10, null=True),
        ),
    ]