# Generated by Django 4.1.5 on 2023-02-01 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('protocol', '0007_fluid_fluid_rate_increment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fluid',
            name='fluid_rate_increment',
            field=models.CharField(default='', max_length=50),
        ),
    ]