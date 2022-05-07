# Generated by Django 3.2.13 on 2022-05-06 09:10

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0005_merge_0003_auto_20220429_0847_0004_grouppermission'),
    ]

    operations = [
        migrations.CreateModel(
            name='GithubUser',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True, verbose_name='UUID')),
                ('is_del', models.BooleanField(default=False, verbose_name='是否删除')),
                ('is_active', models.BooleanField(default=True, verbose_name='是否可用')),
                ('updated', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('github_user_id', models.CharField(blank=True, max_length=255, verbose_name='Github ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.user')),
            ],
        ),
    ]