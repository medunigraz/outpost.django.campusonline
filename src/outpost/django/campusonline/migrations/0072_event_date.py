# Generated by Django 2.2.28 on 2023-02-24 07:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = []

    operations = []
    ops = [
        (
            """
            DROP INDEX IF EXISTS campusonline_event_id_idx;
            """,
            """
            CREATE UNIQUE INDEX campusonline_event_id_idx ON "public"."campusonline_event" ("id");
            """,
        ),
        (
            """
            DROP MATERIALIZED VIEW IF EXISTS "public"."campusonline_event";
            """,
            """
            CREATE MATERIALIZED VIEW "public"."campusonline_event" AS SELECT
                md5(concat(reihung,typ,titel,datum,zeit_von,zeit_bis,pk_geb,pk_raum)) AS id,
                pk_lv::integer AS course_id,
                reihung::integer AS order,
                typ AS category,
                titel AS title,
                datum AS date,
                zeit_von AS start,
                zeit_bis AS end,
                pk_geb::integer AS building_id,
                pk_raum::integer AS room_id,
                anzeige_bis AS show_end
            FROM "campusonline"."veranstaltungen"
            WITH DATA;
            """,
        ),
        (
            """
            CREATE MATERIALIZED VIEW "public"."campusonline_event" AS SELECT
                md5(concat(pk_vl,reihung,typ,titel,datum,zeit_von,zeit_bis,pk_geb,pk_raum,anzeige_bis)) AS id,
                pk_lv::integer AS course_id,
                reihung::integer AS order,
                typ AS category,
                titel AS title,
                datum::date AS date,
                zeit_von AS start,
                zeit_bis AS end,
                pk_geb::integer AS building_id,
                pk_raum::integer AS room_id,
                anzeige_bis AS show_end
            FROM "campusonline"."veranstaltungen"
            WITH DATA;
            """,
            """
            DROP MATERIALIZED VIEW IF EXISTS "public"."campusonline_event";
            """,
        ),
        (
            """
            CREATE UNIQUE INDEX campusonline_event_id_idx ON "public"."campusonline_event" ("id");
            """,
            """
            DROP INDEX IF EXISTS campusonline_event_id_idx;
            """,
        ),
    ]

    dependencies = [
        ("campusonline", "0071_exam_examinee_examineestatus_exammode_examtype"),
    ]

    operations = [
        migrations.RunSQL(
            [forward for forward, reverse in ops],
            [reverse for forward, reverse in reversed(ops)],
        )
    ]
