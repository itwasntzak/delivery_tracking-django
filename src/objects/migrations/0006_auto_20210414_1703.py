# Generated by Django 3.1.7 on 2021-04-14 23:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0005_auto_20210414_1635'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='extrastop',
            name='daily_id',
        ),
        migrations.RemoveField(
            model_name='shift',
            name='daily_extra_stop_id',
        ),
    ]
