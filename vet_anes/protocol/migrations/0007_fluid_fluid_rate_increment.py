# Generated by Django 4.1.5 on 2023-02-01 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('protocol', '0006_fluid'),
    ]

    operations = [
        migrations.AddField(
            model_name='fluid',
            name='fluid_rate_increment',
            field=models.CharField(default='', max_length=20),
        ),
    ]