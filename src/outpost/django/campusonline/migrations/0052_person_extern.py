# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-09-15 07:45
from __future__ import unicode_literals

from django.db import migrations
from django.conf import settings


class Migration(migrations.Migration):

    ops = [
        (
            """
            CREATE FOREIGN TABLE "campusonline"."externe" (
                PERS_NR numeric,
                PERS_FAMNAM varchar,
                PERS_VORNAME varchar,
                PERS_TITEL varchar,
                PERS_SEX varchar,
                PERS_BENUTZERNAME varchar
            )
            SERVER sqlalchemy OPTIONS (
                tablename 'PERSONEN_EXTERN_V',
                db_url '{}'
            );
            """.format(
                settings.MULTICORN.get("campusonline")
            ),
            """
            DROP FOREIGN TABLE IF EXISTS "campusonline"."externe";
            """,
        ),
        (
            """
            CREATE MATERIALIZED VIEW "public"."campusonline_external" AS SELECT
                PERS_NR::integer AS id,
                PERS_FAMNAM AS last_name,
                PERS_VORNAME AS first_name,
                PERS_TITEL AS title,
                PERS_SEX AS sex,
                PERS_BENUTZERNAME AS username
            FROM "campusonline"."externe"
            WITH DATA;
            """,
            """
            DROP MATERIALIZED VIEW IF EXISTS "public"."campusonline_external";
            """,
        ),
        (
            """
            CREATE INDEX campusonline_external_id_idx ON "public"."campusonline_external" ("id");
            """,
            """
            DROP INDEX IF EXISTS campusonline_external_id_idx;
            """,
        ),
        (
            """
            CREATE INDEX campusonline_external_username_idx ON "public"."campusonline_external" ("username");
            """,
            """
            DROP INDEX IF EXISTS campusonline_external_username_idx;
            """,
        ),
    ]

    dependencies = [("campusonline", "0051_distributionlist_union")]

    operations = [
        migrations.RunSQL(
            [forward for forward, reverse in ops],
            [reverse for forward, reverse in reversed(ops)],
        )
    ]
