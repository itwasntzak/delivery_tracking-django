# Generated by Django 3.2.3 on 2021-06-04 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0007_auto_20210414_1742'),
    ]

    operations = [
        migrations.AddField(
            model_name='split',
            name='note',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]