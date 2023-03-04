# Generated by Django 3.0.5 on 2023-03-04 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0021_appointment_prescription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataentryoperator',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pic/DataEntryOperatorProfilePic/'),
        ),
        migrations.AlterField(
            model_name='frontdeskoperator',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pic/FrontDeskOperatorProfilePic/'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='status',
            field=models.PositiveIntegerField(default=0),
        ),
    ]