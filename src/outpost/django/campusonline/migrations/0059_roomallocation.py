# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-09-03 11:12
from __future__ import unicode_literals

from django.db import migrations
from django.conf import settings


class Migration(migrations.Migration):

    ops = [
        (
            """
            CREATE FOREIGN TABLE "campusonline"."hybrid_angemeldete" (
                TERMIN_NR numeric,
                RAUM_NR numeric,
                DATUM_VON timestamptz,
                DATUM_BIS timestamptz,
                ST_PERSON_NR numeric,
                ANGEMELDET varchar
            )
            SERVER sqlalchemy OPTIONS (
                tablename 'LV_HYBRID_ANGEMELDETE_STUD_JE_ZEIT_V',
                db_url '{}'
            );
            """.format(
                settings.MULTICORN.get("campusonline")
            ),
            """
            DROP FOREIGN TABLE IF EXISTS "campusonline"."hybrid_angemeldete";
            """,
        ),
        (
            """
            CREATE MATERIALIZED VIEW "public"."campusonline_roomallocation" AS
            SELECT
                CONCAT_WS(
                    '-'::text,
                    ha.termin_nr::integer,
                    ha.raum_nr::integer,
                    ha.st_person_nr::integer
                ) AS id,
                ha.termin_nr::integer AS term,
                ha.raum_nr::integer AS room_id,
                ha.st_person_nr::integer AS student_id,
                MIN(lgt.lv_beginn) AS start,
                MAX(lgt.lv_ende) AS "end",
                UPPER(ha.angemeldet::text) = 'J'::text AS onsite
            FROM
                campusonline.hybrid_angemeldete ha,
                campusonline.lv_grp_term lgt
            WHERE
                ha.termin_nr = lgt.termin_nr
            GROUP BY
                ha.termin_nr,
                ha.raum_nr,
                ha.st_person_nr,
                ha.angemeldet
            WITH DATA;
            """,
            """
            DROP MATERIALIZED VIEW IF EXISTS "public"."campusonline_roomallocation";
            """,
        ),
        (
            """
            CREATE INDEX campusonline_roomallocation_id_idx ON "public"."campusonline_roomallocation" ("id");
            """,
            """
            DROP INDEX IF EXISTS campusonline_roomallocation_id_idx;
            """,
        ),
        (
            """
            CREATE INDEX campusonline_roomallocation_room_id_idx ON "public"."campusonline_roomallocation" ("room_id");
            """,
            """
            DROP INDEX IF EXISTS campusonline_roomallocation_room_id_idx;
            """,
        ),
        (
            """
            CREATE INDEX campusonline_roomallocation_student_id_idx ON "public"."campusonline_roomallocation" ("student_id");
            """,
            """
            DROP INDEX IF EXISTS campusonline_roomallocation_student_id_idx;
            """,
        ),
        (
            """
            CREATE INDEX campusonline_roomallocation_timerange_idx ON "public"."campusonline_roomallocation" ("start", "end");
            """,
            """
            DROP INDEX IF EXISTS campusonline_roomallocation_timerange_idx;
            """,
        ),
    ]

    dependencies = [
        ('campusonline', '0058_student_email'),
    ]

    operations = [
        migrations.RunSQL(
            [forward for forward, reverse in ops],
            [reverse for forward, reverse in reversed(ops)],
        )
    ]