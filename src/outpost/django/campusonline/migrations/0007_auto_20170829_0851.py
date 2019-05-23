# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-29 06:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("campusonline", "0006_auto_20170828_1425")]

    forward = [
        """
        DROP MATERIALIZED VIEW IF EXISTS "public"."campusonline_room";
        """,
        """
        CREATE MATERIALIZED VIEW "public"."campusonline_room" AS SELECT
            raum_nr ::integer AS id,
            raum_bez AS title,
            gebaeude_nr ::integer AS building_id,
            stockwerk_nr ::integer AS floor_id,
            raum AS name_short,
            raum_nummer AS name_full,
            flaeche AS area,
            hoehe AS height,
            org_nr ::integer AS organization_id,
            raumtyp ::integer AS category_id
        FROM "campusonline"."raum"
        WITH DATA;
        """,
    ]

    reverse = [
        """
        DROP MATERIALIZED VIEW IF EXISTS "public"."campusonline_room";
        """,
        """
        CREATE MATERIALIZED VIEW "public"."campusonline_room" AS SELECT
            raum_nr ::integer AS id,
            raum_bez AS title,
            gebaeude_nr ::integer AS building_id,
            stockwerk_nr ::integer AS floor_id,
            raum AS name_short,
            raum_nummer AS name_full,
            flaeche AS area,
            hoehe AS height,
            CASE
                org_nr
            WHEN
                1
            THEN
                NULL
            ELSE
                org_nr ::integer
            END AS organization_id,
            raumtyp ::integer AS category_id
        FROM "campusonline"."raum"
        WITH DATA;
        """,
    ]

    operations = [migrations.RunSQL(forward, reverse)]
