# Generated by Django 3.0.8 on 2020-07-23 17:21

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0006_category_crawledlinks_keyword_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='crawledlinks',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]