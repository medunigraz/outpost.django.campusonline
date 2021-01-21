# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-12-02 21:07
from __future__ import unicode_literals

from django.db import migrations
from django.conf import settings


class Migration(migrations.Migration):

    ops = [
        (
            """
            DROP INDEX IF EXISTS campusonline_person_last_name_idx;
            """,
            """
            CREATE INDEX campusonline_person_last_name_idx ON "public"."campusonline_person" ("last_name");
            """,
        ),
        (
            """
            DROP INDEX IF EXISTS campusonline_person_first_name_idx;
            """,
            """
            CREATE INDEX campusonline_person_first_name_idx ON "public"."campusonline_person" ("first_name");
            """,
        ),
        (
            """
            DROP INDEX IF EXISTS campusonline_person_sex_idx;
            """,
            """
            CREATE INDEX campusonline_person_sex_idx ON "public"."campusonline_person" ("sex");
            """,
        ),
        (
            """
            DROP INDEX IF EXISTS campusonline_person_hash_idx;
            """,
            """
            CREATE UNIQUE INDEX campusonline_person_hash_idx ON "public"."campusonline_person" ("hash");
            """,
        ),
        (
            """
            DROP INDEX IF EXISTS campusonline_person_email_idx;
            """,
            """
            CREATE UNIQUE INDEX campusonline_person_email_idx ON "public"."campusonline_person" ("email");
            """,
        ),
        (
            """
            DROP INDEX IF EXISTS campusonline_person_id_idx;
            """,
            """
            CREATE UNIQUE INDEX campusonline_person_id_idx ON "public"."campusonline_person" ("id");
            """,
        ),
        (
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
                p.pers_email AS email,
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
                END AS hash,
                p.tel_nr AS phone,
                p.mobil_tel_nr AS mobile,
                CASE
                    LOWER(p.dv)
                WHEN
                    'j'
                THEN
                    true
                ELSE
                    false
                END AS employed
            FROM
                "campusonline"."personen" p
            LEFT JOIN
                "campusonline"."personen_profilbilder_daten" ppd
            ON
                p.pers_nr::integer = ppd.person_nr::integer
            WITH DATA;
            """,
        ),
        (
            """
            ALTER FOREIGN TABLE "campusonline"."personen" ADD COLUMN VISITENKARTE varchar;
            """,
            """
            ALTER FOREIGN TABLE "campusonline"."personen" DROP COLUMN VISITENKARTE;
            """,
        ),
        (
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
                p.pers_email AS email,
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
                END AS hash,
                p.tel_nr AS phone,
                p.mobil_tel_nr AS mobile,
                CASE
                    LOWER(p.dv)
                WHEN
                    'j'
                THEN
                    true
                ELSE
                    false
                END AS employed,
                p.visitenkarte AS card
            FROM
                "campusonline"."personen" p
            LEFT JOIN
                "campusonline"."personen_profilbilder_daten" ppd
            ON
                p.pers_nr::integer = ppd.person_nr::integer
            WITH DATA;
            """,
            """
            DROP MATERIALIZED VIEW IF EXISTS "public"."campusonline_person";
            """,
        ),
        (
            """
            CREATE UNIQUE INDEX campusonline_person_hash_idx ON "public"."campusonline_person" ("hash");
            """,
            """
            DROP INDEX IF EXISTS campusonline_person_hash_idx;
            """,
        ),
        (
            """
            CREATE UNIQUE INDEX campusonline_person_email_idx ON "public"."campusonline_person" ("email");
            """,
            """
            DROP INDEX IF EXISTS campusonline_person_email_idx;
            """,
        ),
        (
            """
            CREATE UNIQUE INDEX campusonline_person_id_idx ON "public"."campusonline_person" ("id");
            """,
            """
            DROP INDEX IF EXISTS campusonline_person_id_idx;
            """,
        ),
        (
            """
            CREATE INDEX campusonline_person_sex_idx ON "public"."campusonline_person" ("sex");
            """,
            """
            DROP INDEX IF EXISTS campusonline_person_sex_idx;
            """,
        ),
        (
            """
            CREATE INDEX campusonline_person_first_name_idx ON "public"."campusonline_person" ("first_name");
            """,
            """
            DROP INDEX IF EXISTS campusonline_person_first_name_idx;
            """,
        ),
        (
            """
            CREATE INDEX campusonline_person_last_name_idx ON "public"."campusonline_person" ("last_name");
            """,
            """
            DROP INDEX IF EXISTS campusonline_person_last_name_idx;
            """,
        ),
        (
            """
            CREATE INDEX campusonline_person_employed_idx ON "public"."campusonline_person" ("employed");
            """,
            """
            DROP INDEX IF EXISTS campusonline_person_employed_idx;
            """,
        ),
    ]

    dependencies = [("campusonline", "0053_external")]

    operations = [
        migrations.RunSQL(
            [forward for forward, reverse in ops],
            [reverse for forward, reverse in reversed(ops)],
        )
    ]
