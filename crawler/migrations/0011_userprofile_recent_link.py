# Generated by Django 3.0.8 on 2020-08-03 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0010_auto_20200727_1055'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='recent_link',
            field=models.IntegerField(default=5),
        ),
    ]
