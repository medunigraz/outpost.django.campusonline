# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-28 08:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("campusonline", "0008_courses")]

    operations = [
        migrations.CreateModel(
            name="Course",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=256)),
                ("category", models.CharField(max_length=256)),
                ("year", models.CharField(max_length=256)),
                ("semester", models.CharField(max_length=256)),
            ],
            options={"managed": False, "db_table": "campusonline_course"},
        ),
        migrations.CreateModel(
            name="CourseGroup",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=256)),
            ],
            options={"managed": False, "db_table": "campusonline_coursegroup"},
        ),
        migrations.CreateModel(
            name="CourseGroupTerm",
            fields=[
                (
                    "id",
                    models.CharField(max_length=128, primary_key=True, serialize=False),
                ),
                ("start", models.DateTimeField()),
                ("end", models.DateTimeField()),
            ],
            options={"managed": False, "db_table": "campusonline_coursegroupterm"},
        ),
        migrations.CreateModel(
            name="Student",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                (
                    "matriculation",
                    models.CharField(blank=True, max_length=16, null=True),
                ),
                ("first_name", models.CharField(max_length=256)),
                ("last_name", models.CharField(max_length=256)),
                ("title", models.CharField(blank=True, max_length=256, null=True)),
                ("cardid", models.CharField(blank=True, max_length=16, null=True)),
            ],
            options={"managed": False, "db_table": "campusonline_student"},
        ),
    ]
