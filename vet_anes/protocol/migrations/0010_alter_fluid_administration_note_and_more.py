# Generated by Django 4.1.5 on 2023-02-02 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('protocol', '0009_fluid_administration_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fluid',
            name='administration_note',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='fluid',
            name='fluid_rate_increment',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
    ]
