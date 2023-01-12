# Generated by Django 2.2.28 on 2022-11-08 13:12

from django.db import migrations
from django.conf import settings


class Migration(migrations.Migration):

    ops = [
        (
            """
            CREATE FOREIGN TABLE "campusonline"."laender_iso" (
                ISO_NUMMER varchar,
                ISO_CODE_2 varchar,
                ISO_CODE_3 varchar,
                NAME_DE varchar,
                NAME_EN varchar
            )
            SERVER sqlalchemy OPTIONS (
                tablename 'LAENDER_ISO_V',
                primary_key 'ISO_NUMMER',
                db_url '{}'
            );
            """.format(
                settings.MULTICORN.get("campusonline")
            ),
            """
            DROP FOREIGN TABLE IF EXISTS "campusonline"."laender_iso";
            """,
        ),
        (
            """
            CREATE MATERIALIZED VIEW "public"."campusonline_country" AS SELECT
                iso_code_2 AS alpha2,
                iso_code_3 AS alpha3,
                hstore(
                    array['de', 'en'],
                    array[name_de, name_en]
                ) AS name
            FROM
                campusonline.laender_iso
            WHERE
                iso_code_2 IS NOT NULL AND
                iso_code_3 IS NOT NULL AND
                iso_code_2 ~ '^[A-Z]{2}$' AND
                iso_code_3 ~ '^[A-Z]{3}$'
            WITH DATA;
            """,
            """
            DROP MATERIALIZED VIEW IF EXISTS "public"."campusonline_country";
            """,
        ),
    ]

    dependencies = [
        ("campusonline", "0065_auto_20221021_2308"),
    ]

    operations = [
        migrations.RunSQL(
            [forward for forward, reverse in ops],
            [reverse for forward, reverse in reversed(ops)],
        )
    ]
