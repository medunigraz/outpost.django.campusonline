# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-25 17:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("campusonline", "0014_stud_lv_anw")]

    operations = [
        migrations.AlterModelOptions(
            name="coursegroupterm",
            options={
                "managed": False,
                "ordering": ("start", "end"),
                "permissions": (
                    ("view_coursegroupterm", "Can view course group term"),
                ),
            },
        )
    ]
