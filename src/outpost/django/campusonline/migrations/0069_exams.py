# Generated by Django 2.2.28 on 2023-01-30 12:23

from django.db import migrations
from django.conf import settings


class Migration(migrations.Migration):

    ops = [
        (
            """
            CREATE FOREIGN TABLE "campusonline"."pv_termine" (
                TERMIN_NR integer,
                ORG_NR integer,
                PV_PR_MOD_NR integer,
                PV_PR_TYP_NR integer,
                PRUEFER_PERSON_NR integer,
                STP_SP_NR integer,
                ANMELDE_BEGINN timestamp,
                ANMELDE_ENDE timestamp,
                BEGINN_ZEIT timestamp,
                WEBANMELDUNGS_FLAG varchar,
                ANMERKUNG text,
                TERMIN_GUELTIG_FLAG varchar,
                ABMELDE_ENDE timestamp,
                ORT text
            )
            SERVER sqlalchemy OPTIONS (
                tablename 'PV_TERMINE_V',
                primary_key 'TERMIN_NR',
                db_url '{}'
            );
            """.format(
                settings.MULTICORN.get("campusonline")
            ),
            """
            DROP FOREIGN TABLE IF EXISTS "campusonline"."pv_termine";
            """,
        ),
        (
            """
            CREATE FOREIGN TABLE "campusonline"."pv_kandidaten" (
                KANDIDATEN_NR integer,
                TERMIN_NR integer,
                ST_PERSON_NR integer,
                STATUS_DATUM timestamp,
                PV_PST_TYP_NR integer,
                ANMELDE_DATUM timestamp,
                DATUM_DER_LETZTBEURTEILUNG timestamp
            )
            SERVER sqlalchemy OPTIONS (
                tablename 'PV_KANDIDATEN_V',
                primary_key 'TERMIN_NR',
                db_url '{}'
            );
            """.format(
                settings.MULTICORN.get("campusonline")
            ),
            """
            DROP FOREIGN TABLE IF EXISTS "campusonline"."pv_kandidaten";
            """,
        ),
        (
            """
            CREATE FOREIGN TABLE "campusonline"."pv_pruefungs_modi" (
                NR integer,
                KURZBEZEICHNUNG varchar,
                NAME varchar,
                NAME_ENGL varchar
            )
            SERVER sqlalchemy OPTIONS (
                tablename 'PV_PRUEFUNGSMODI_V',
                primary_key 'NR',
                db_url '{}'
            );
            """.format(
                settings.MULTICORN.get("campusonline")
            ),
            """
            DROP FOREIGN TABLE IF EXISTS "campusonline"."pv_pruefungs_modi";
            """,
        ),
        (
            """
            CREATE FOREIGN TABLE "campusonline"."pv_pruefungs_typen" (
                NR integer,
                KURZBEZEICHNUNG varchar,
                ZEUGNISBEZEICHNUNG varchar,
                ZEUGNISBEZEICHNUNG_ENGL varchar,
                NAME varchar,
                NAME_ENGL varchar
            )
            SERVER sqlalchemy OPTIONS (
                tablename 'PV_PRUEFUNGSTYPEN_V',
                primary_key 'NR',
                db_url '{}'
            );
            """.format(
                settings.MULTICORN.get("campusonline")
            ),
            """
            DROP FOREIGN TABLE IF EXISTS "campusonline"."pv_pruefungs_typen";
            """,
        ),
        (
            """
            CREATE FOREIGN TABLE "campusonline"."pv_pruef_status_typen" (
                NR integer,
                KURZBEZEICHNUNG varchar,
                NAME text
            )
            SERVER sqlalchemy OPTIONS (
                tablename 'PV_PRUEFSTATUS',
                primary_key 'NR',
                db_url '{}'
            );
            """.format(
                settings.MULTICORN.get("campusonline")
            ),
            """
            DROP FOREIGN TABLE IF EXISTS "campusonline"."pv_pruef_status_typen";
            """,
        ),
        (
            """
            CREATE MATERIALIZED VIEW "public"."campusonline_exam_mode" AS SELECT
                NR AS id,
                KURZBEZEICHNUNG AS short,
                HSTORE(
                    array['de', 'en'],
                    array[NAME, NAME_ENGL]
                ) AS name
            FROM
                campusonline.pv_pruefungs_modi
            WITH DATA;
            """,
            """
            DROP MATERIALIZED VIEW IF EXISTS "public"."campusonline_exam_mode";
            """,
        ),
        (
            """
            CREATE MATERIALIZED VIEW "public"."campusonline_exam_type" AS SELECT
                NR AS id,
                KURZBEZEICHNUNG AS short,
                HSTORE(
                    array['de', 'en'],
                    array[ZEUGNISBEZEICHNUNG, ZEUGNISBEZEICHNUNG_ENGL]
                ) AS certificate,
                HSTORE(
                    array['de', 'en'],
                    array[NAME, NAME_ENGL]
                ) AS name
            FROM
                campusonline.pv_pruefungs_typen
            WITH DATA;
            """,
            """
            DROP MATERIALIZED VIEW IF EXISTS "public"."campusonline_exam_type";
            """,
        ),
        (
            """
            CREATE MATERIALIZED VIEW "public"."campusonline_examinee_status" AS SELECT
                NR AS id,
                KURZBEZEICHNUNG AS short,
                HSTORE(
                    array['de'],
                    array[NAME]
                ) AS name
            FROM
                campusonline.pv_pruef_status_typen
            WITH DATA;
            """,
            """
            DROP MATERIALIZED VIEW IF EXISTS "public"."campusonline_examinee_status";
            """,
        ),
        (
            """
            CREATE MATERIALIZED VIEW "public"."campusonline_exam" AS SELECT
                TERMIN_NR AS id,
                ORG_NR AS organization_id,
                PV_PR_MOD_NR AS mode_id,
                PV_PR_TYP_NR AS type_id,
                PRUEFER_PERSON_NR AS examiner_id,
                STP_SP_NR AS course_id,
                ANMELDE_BEGINN AT TIME ZONE '{tz}' AS registration_start,
                ANMELDE_ENDE AT TIME ZONE '{tz}' AS registration_end,
                BEGINN_ZEIT AT TIME ZONE '{tz}' AS start,
                LOWER(WEBANMELDUNGS_FLAG) = 'j' AS online_registration,
                ANMERKUNG AS note,
                LOWER(TERMIN_GUELTIG_FLAG) = 'j' AS valid,
                ABMELDE_ENDE AT TIME ZONE '{tz}' AS deregistration_end,
                ORT AS location
            FROM
                campusonline.pv_termine
            WITH DATA;
            """.format(
                tz=settings.TIME_ZONE
            ),
            """
            DROP MATERIALIZED VIEW IF EXISTS "public"."campusonline_exam";
            """,
        ),
        (
            """
            CREATE MATERIALIZED VIEW "public"."campusonline_examinee" AS SELECT
                KANDIDATEN_NR AS id,
                TERMIN_NR AS exam_id,
                ST_PERSON_NR AS student_id,
                STATUS_DATUM AT TIME ZONE '{tz}' AS status_datetime,
                PV_PST_TYP_NR AS status_id,
                DATE(ANMELDE_DATUM) AS registration,
                DATE(DATUM_DER_LETZTBEURTEILUNG) AS assessment_closure
            FROM
                campusonline.pv_kandidaten
            WITH DATA;
            """.format(
                tz=settings.TIME_ZONE
            ),
            """
            DROP MATERIALIZED VIEW IF EXISTS "public"."campusonline_examinee";
            """,
        ),
    ]

    dependencies = [
        ("campusonline", "0068_lw_anv_lehrender"),
    ]

    operations = [
        migrations.RunSQL(
            [forward for forward, reverse in ops],
            [reverse for forward, reverse in reversed(ops)],
        )
    ]
