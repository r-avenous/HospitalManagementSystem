# Generated by Django 3.0.5 on 2023-03-03 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0020_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='prescription',
            field=models.TextField(default=0, max_length=500),
            preserve_default=False,
        ),
    ]
