# Generated by Django 3.0.8 on 2020-07-31 10:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0002_auto_20200731_0856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rescrapedlink',
            name='link',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scheduler.ScrapedLink'),
        ),
    ]
