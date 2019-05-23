# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-08-31 09:52
from __future__ import unicode_literals

from django.db import migrations
from django.conf import settings


class Migration(migrations.Migration):

    forward = [
        """
        DROP MATERIALIZED VIEW IF EXISTS "public"."campusonline_function";
        """,
        """
        DROP FOREIGN TABLE IF EXISTS "campusonline"."funktionen";
        """,
        """
        CREATE FOREIGN TABLE "campusonline"."funktionen" (
            FUNK_NR numeric,
            FUNK_BEZ varchar,
            FUNK_GRUPPE varchar,
            FUNK_LEITER varchar,
            FUNK_NAME_W varchar,
            FUNK_NAME_M varchar
        )
        SERVER sqlalchemy OPTIONS (
            tablename 'FUNKTIONEN_V',
            db_url '{}'
        );
        """.format(
            settings.MULTICORN.get("campusonline")
        ),
        """
        CREATE MATERIALIZED VIEW "public"."campusonline_function" AS SELECT
            funk_nr::integer AS id,
            funk_bez AS name,
            funk_gruppe AS category,
            (CASE upper(funk_leiter) WHEN 'X' THEN TRUE ELSE FALSE END)::boolean AS leader,
            funk_name_w AS name_female,
            funk_name_m AS name_male
        FROM "campusonline"."funktionen"
        WITH DATA;
        """,
    ]
    reverse = [
        """
        DROP MATERIALIZED VIEW IF EXISTS "public"."campusonline_function";
        """,
        """
        DROP FOREIGN TABLE IF EXISTS "campusonline"."funktionen";
        """,
    ]

    dependencies = [("campusonline", "0030_distributionlist")]

    operations = [migrations.RunSQL(forward, reverse)]
