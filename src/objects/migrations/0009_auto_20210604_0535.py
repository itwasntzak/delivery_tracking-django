# Generated by Django 3.2.3 on 2021-06-04 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0008_split_note'),
    ]

    operations = [
        migrations.AddField(
            model_name='shift',
            name='daily_split_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='split',
            name='daily_id',
            field=models.IntegerField(default=0),
        ),
    ]