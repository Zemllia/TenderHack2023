# Generated by Django 4.2.6 on 2023-11-17 21:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TenderHack', '0002_remove_company_kpp_kpp'),
    ]

    operations = [
        migrations.CreateModel(
            name='CPGS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, verbose_name='Код')),
                ('name', models.CharField(max_length=255, verbose_name='Наименование')),
                ('full_path', models.CharField(max_length=255, verbose_name='Полный путь')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='TenderHack.cpgs', verbose_name='Родительский КПГЗ')),
            ],
        ),
    ]