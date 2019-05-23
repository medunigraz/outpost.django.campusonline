# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-13 11:11
from __future__ import unicode_literals

from django.db import migrations
from django.conf import settings


class Migration(migrations.Migration):

    forward = [
        """
        CREATE FOREIGN TABLE "campusonline"."personen_profilbilder_daten" (
            PERSON_NR numeric,
            CONTENT bytea
        )
        SERVER sqlalchemy OPTIONS (
            tablename 'PERSONEN_PROFILBILDER_DATEN_V',
            db_url '{}'
        );
        """.format(
            settings.MULTICORN.get("campusonline")
        ),
        """
        DROP MATERIALIZED VIEW IF EXISTS "public"."campusonline_person";
        """,
        """
        CREATE MATERIALIZED VIEW "public"."campusonline_person" AS SELECT
            p.pers_nr::integer AS id,
            p.pers_vorname AS first_name,
            p.pers_famnam AS last_name,
            p.pers_titel AS title,
            p.pers_sex AS sex,
            p.pers_benutzername AS username,
            p.pers_sprechstunde AS consultation,
            p.pers_zusatz_info AS appendix,
            p.pers_profilbild AS avatar,
            p.raum_nr::integer AS room_id,
            ppd.content AS avatar_private,
            CASE
                ppd.content
            WHEN
                NULL
            THEN
                NULL
            ELSE
                encode(digest(format('%s-%s-', p.pers_nr, p.pers_benutzername)::bytea || ppd.content, 'sha1'), 'hex')
            END AS hash
        FROM
            "campusonline"."personen" p
        LEFT JOIN
            "campusonline"."personen_profilbilder_daten" ppd
        ON
            p.pers_nr::integer = ppd.person_nr::integer
        WITH DATA;
        """,
        """
        CREATE UNIQUE INDEX campusonline_person_hash_idx ON "public"."campusonline_person" ("hash");
        """,
    ]
    reverse = [
        """
        DROP INDEX IF EXISTS campusonline_person_avatar_private_hash_idx;
        """,
        """
        DROP MATERIALIZED VIEW IF EXISTS "public"."campusonline_person";
        """,
        """
        CREATE MATERIALIZED VIEW "public"."campusonline_person" AS SELECT
            pers_nr ::integer AS id,
            pers_vorname AS first_name,
            pers_famnam AS last_name,
            pers_titel AS title,
            pers_sex AS sex,
            pers_benutzername AS username,
            pers_sprechstunde AS consultation,
            pers_zusatz_info AS appendix,
            pers_profilbild AS avatar,
            raum_nr ::integer AS room_id
        FROM "campusonline"."personen"
        WITH DATA;
        """,
        """
        DROP FOREIGN TABLE IF EXISTS "campusonline"."personen_profilbilder_daten";
        """,
    ]

    dependencies = [("campusonline", "0032_person_organization")]

    operations = [migrations.RunSQL(forward, reverse)]
