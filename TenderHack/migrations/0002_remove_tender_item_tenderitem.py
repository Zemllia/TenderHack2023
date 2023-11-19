# Generated by Django 4.2.6 on 2023-11-18 06:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TenderHack', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tender',
            name='item',
        ),
        migrations.CreateModel(
            name='TenderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('tender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='TenderHack.tender', verbose_name='Тендер')),
            ],
        ),
    ]