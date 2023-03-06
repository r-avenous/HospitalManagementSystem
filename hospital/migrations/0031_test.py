# Generated by Django 4.1.7 on 2023-03-06 10:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("hospital", "0030_remove_appointment_appointmentdate_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Test",
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
                ("doctername", models.CharField(max_length=40)),
                ("procedurename", models.CharField(max_length=40)),
                ("description", models.TextField(max_length=500, null=True)),
                (
                    "image",
                    models.ImageField(blank=True, null=True, upload_to="testimages/"),
                ),
                (
                    "patientId",
                    models.ForeignKey(
                        default=0,
                        on_delete=django.db.models.deletion.SET_DEFAULT,
                        to="hospital.patient",
                        verbose_name="id",
                    ),
                ),
            ],
        ),
    ]
