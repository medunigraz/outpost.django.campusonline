# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-08 12:24
from __future__ import unicode_literals

from django.db import migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [("campusonline", "0010_auto_20171002_1450")]

    forward = [
        """
        CREATE FOREIGN TABLE "campusonline"."veranstaltungen" (
            PK_LV numeric,
            REIHUNG numeric,
            TYP varchar,
            NUMMER varchar,
            TITEL varchar,
            DATUM timestamptz,
            ZEIT_VON timestamptz,
            ZEIT_BIS timestamptz,
            PK_GEB numeric,
            GEBAEUDE varchar,
            PK_RAUM numeric,
            RAUM varchar,
            RAUM_BEZ varchar,
            TERMINART varchar,
            ANZEIGE_BIS timestamptz
        )
        SERVER sqlalchemy OPTIONS (
            tablename 'VERANSTALTUNGEN_HEUTE_V',
            db_url '{}'
        );
        """.format(
            settings.MULTICORN.get("campusonline")
        ),
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
    ]

    reverse = [
        """
        DROP MATERIALIZED VIEW IF EXISTS "public"."campusonline_event";
        """,
        """
        DROP FOREIGN TABLE IF EXISTS "campusonline"."veranstaltungen";
        """,
    ]
    operations = [migrations.RunSQL(forward, reverse)]
