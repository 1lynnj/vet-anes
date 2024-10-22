# Generated by Django 4.1.5 on 2023-02-01 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('protocol', '0005_drug_er_dose'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fluid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('rate_name', models.CharField(max_length=50)),
                ('type', models.CharField(max_length=50)),
                ('cat_rate_calculation', models.IntegerField()),
                ('dog_rate_calculation', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
