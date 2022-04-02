# Generated by Django 4.0.3 on 2022-04-01 10:20

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='App',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True, verbose_name='UUID')),
                ('is_del', models.BooleanField(default=False, verbose_name='是否删除')),
                ('is_active', models.BooleanField(default=True, verbose_name='是否可用')),
                ('updated', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('name', models.CharField(max_length=128, verbose_name='应用名称')),
                ('url', models.CharField(blank=True, max_length=1024, verbose_name='应用地址')),
                ('logo', models.CharField(blank=True, default='', max_length=1024, null=True, verbose_name='应用图标')),
                ('description', models.TextField(blank=True, null=True, verbose_name='应用描述')),
                ('type', models.CharField(max_length=128, verbose_name='应用类型')),
                ('data', models.JSONField(blank=True, default=dict, verbose_name='应用配置')),
                ('secret', models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='应用密钥')),
            ],
            options={
                'verbose_name': '应用',
                'verbose_name_plural': '应用',
            },
            managers=[
                ('expand_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True, verbose_name='UUID')),
                ('is_del', models.BooleanField(default=False, verbose_name='是否删除')),
                ('is_active', models.BooleanField(default=True, verbose_name='是否可用')),
                ('updated', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('name', models.CharField(max_length=128, verbose_name='名字')),
                ('slug', models.SlugField(unique=True, verbose_name='短链接标识')),
                ('icon', models.URLField(blank=True, verbose_name='图标')),
            ],
            options={
                'verbose_name': '租户',
                'verbose_name_plural': '租户',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True, verbose_name='UUID')),
                ('is_del', models.BooleanField(default=False, verbose_name='是否删除')),
                ('is_active', models.BooleanField(default=True, verbose_name='是否可用')),
                ('updated', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('username', models.CharField(max_length=128)),
                ('avatar', models.URLField(blank=True, verbose_name='头像')),
                ('is_platform_user', models.BooleanField(default=False, verbose_name='是否是平台用户')),
                ('tenants', models.ManyToManyField(related_name='user_tenant_set', related_query_name='tenant', to='core.tenant')),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
            },
            managers=[
                ('expand_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True, verbose_name='UUID')),
                ('is_del', models.BooleanField(default=False, verbose_name='是否删除')),
                ('is_active', models.BooleanField(default=True, verbose_name='是否可用')),
                ('updated', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('name', models.CharField(max_length=128)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='children', to='core.usergroup')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.tenant')),
                ('users', models.ManyToManyField(blank=True, related_name='user_set', related_query_name='user', to='core.user', verbose_name='用户列表')),
            ],
            options={
                'verbose_name': '用户分组',
                'verbose_name_plural': '用户分组',
            },
            managers=[
                ('expand_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True, verbose_name='UUID')),
                ('is_del', models.BooleanField(default=False, verbose_name='是否删除')),
                ('is_active', models.BooleanField(default=True, verbose_name='是否可用')),
                ('updated', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('name', models.CharField(max_length=255, verbose_name='名称')),
                ('code', models.CharField(max_length=100, verbose_name='编码')),
                ('category', models.CharField(choices=[('entry', '入口'), ('api', 'API'), ('data', '数据'), ('group', '分组'), ('ui', '界面'), ('other', '其它')], default='other', max_length=100, verbose_name='类型')),
                ('is_system', models.BooleanField(default=True, verbose_name='是否是系统权限')),
                ('app', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='core.app', verbose_name='应用')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='children', to='core.permission', verbose_name='父权限分组')),
                ('permissions', models.ManyToManyField(blank=True, related_name='permission_set', related_query_name='permission', to='core.permission', verbose_name='权限列表')),
                ('tenant', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='core.tenant', verbose_name='租户')),
            ],
            options={
                'verbose_name': '权限分组',
                'verbose_name_plural': '权限分组',
            },
            managers=[
                ('expand_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Approve',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True, verbose_name='UUID')),
                ('is_del', models.BooleanField(default=False, verbose_name='是否删除')),
                ('is_active', models.BooleanField(default=True, verbose_name='是否可用')),
                ('updated', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('name', models.CharField(max_length=255, verbose_name='名称')),
                ('code', models.CharField(max_length=100, verbose_name='编码')),
                ('description', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('status', models.CharField(choices=[('wait', '待审批'), ('pass', '通过'), ('deny', '拒绝')], default='wait', max_length=100, verbose_name='状态')),
                ('data', models.JSONField(default=dict, verbose_name='数据')),
                ('app', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='core.app', verbose_name='应用')),
                ('tenant', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='core.tenant', verbose_name='租户')),
            ],
            options={
                'verbose_name': '审批动作',
                'verbose_name_plural': '审批动作',
            },
            managers=[
                ('expand_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='AppGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True, verbose_name='UUID')),
                ('is_del', models.BooleanField(default=False, verbose_name='是否删除')),
                ('is_active', models.BooleanField(default=True, verbose_name='是否可用')),
                ('updated', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('name', models.CharField(max_length=128)),
                ('apps', models.ManyToManyField(blank=True, related_name='app_set', related_query_name='app', to='core.app', verbose_name='应用列表')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='children', to='core.appgroup')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.tenant')),
            ],
            options={
                'verbose_name': '应用分组',
                'verbose_name_plural': '应用分组',
            },
            managers=[
                ('expand_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='app',
            name='tenant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.tenant'),
        ),
    ]