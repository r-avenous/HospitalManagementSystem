# Generated by Django 3.0.5 on 2023-03-04 17:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0023_procedure_room_undergoes'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='dischargeDate',
            field=models.DateField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='room',
            field=models.ForeignKey(default=0, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='hospital.Room', verbose_name='number'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='admitDate',
            field=models.DateField(auto_now=True, null=True),
        ),
    ]