# Generated by Django 2.0.3 on 2018-03-22 16:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.crypto
import django.utils.timezone
import enumfields.fields
import freenodejobs.jobs.enums
import functools


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(default=functools.partial(django.utils.crypto.get_random_string, *(8, 'acefhkjprutwvyx'), **{}), max_length=8, unique=True)),
                ('state', enumfields.fields.EnumIntegerField(default=10, enum=freenodejobs.jobs.enums.StateEnum)),
                ('title', models.CharField(max_length=255)),
                ('job_type', enumfields.fields.EnumIntegerField(enum=freenodejobs.jobs.enums.JobTypeEnum)),
                ('location', models.CharField(max_length=255)),
                ('apply_url', models.URLField()),
                ('description', models.TextField(blank=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created',),
                'get_latest_by': 'created',
            },
        ),
    ]
