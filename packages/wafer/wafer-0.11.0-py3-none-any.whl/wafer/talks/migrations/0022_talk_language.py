# Generated by Django 2.2.23 on 2021-06-03 15:32

from django.conf import settings
from django.db import migrations, models
import wafer.talks.models


class Migration(migrations.Migration):

    dependencies = [
        ('talks', '0021_talk_type_show_speakers'),
    ]

    operations = [
        migrations.AddField(
            model_name='talk',
            name='language',
            field=models.CharField(blank=True, max_length=5, null=True, verbose_name='language'),
        ),
    ]
