# Generated by Django 4.2.6 on 2023-11-17 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TenderHack', '0004_subdivision_remove_company_is_contractor_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='date_created',
            field=models.DateTimeField(default="2023-01-09 00:00", verbose_name='Дата создания'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subdivision',
            name='date_created',
            field=models.DateTimeField(default="2023-01-09 00:00", verbose_name='Дата создания'),
            preserve_default=False,
        ),
    ]