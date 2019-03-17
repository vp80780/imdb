# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2019-03-17 13:17
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('genre', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Movies',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250)),
                ('director', models.CharField(max_length=250)),
                ('imdb_score', models.FloatField()),
                ('popularity', models.FloatField()),
                ('genre', models.ManyToManyField(to='movies.Genre')),
            ],
        ),
    ]
