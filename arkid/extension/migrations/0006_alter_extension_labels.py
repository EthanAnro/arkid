# Generated by Django 3.2.13 on 2022-06-14 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extension', '0005_merge_20220614_1413'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extension',
            name='labels',
            field=models.JSONField(blank=True, default=list, verbose_name='Labels'),
        ),
    ]