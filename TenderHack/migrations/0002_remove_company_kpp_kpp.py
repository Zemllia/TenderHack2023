# Generated by Django 4.2.6 on 2023-11-17 21:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TenderHack', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='kpp',
        ),
        migrations.CreateModel(
            name='Kpp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kpp', models.CharField(blank=True, max_length=9, null=True, verbose_name='КПП')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kpps', to='TenderHack.company', verbose_name='Компания')),
            ],
        ),
    ]
