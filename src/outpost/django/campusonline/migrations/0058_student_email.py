# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-04-08 18:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    ops = [
        (
            """
            DROP INDEX IF EXISTS campusonline_student_cardid_idx;
            """,
            """
            CREATE INDEX campusonline_student_cardid_idx ON "public"."campusonline_student" ("cardid");
            """,
        ),
        (
            """
            DROP INDEX IF EXISTS campusonline_student_matriculation_idx;
            """,
            """
            CREATE INDEX campusonline_student_matriculation_idx ON "public"."campusonline_student" ("matriculation");
            """,
        ),
        (
            """
            DROP INDEX IF EXISTS campusonline_student_id_idx;
            """,
            """
            CREATE INDEX campusonline_student_id_idx ON "public"."campusonline_student" ("id");
            """,
        ),
        (
            """
            DROP INDEX IF EXISTS campusonline_student_username_idx;
            """,
            """
            CREATE INDEX campusonline_student_username_idx ON "public"."campusonline_student" ("username");
            """,
        ),
        (
            """
            DROP MATERIALIZED VIEW IF EXISTS "public"."campusonline_student";
            """,
            """
            CREATE MATERIALIZED VIEW "public"."campusonline_student" AS SELECT
                stud_nr::integer AS id,
                stud_mnr AS matriculation,
                stud_famnam AS last_name,
                stud_vorname AS first_name,
                stud_akadgrad AS title,
                stud_mifare AS cardid,
                stud_benutzername as username,
                pers_profilbild as avatar
            FROM "campusonline"."stud"
            WITH DATA;
            """,
        ),
        (
            """
            ALTER FOREIGN TABLE "campusonline"."stud" ADD COLUMN EMAIL varchar;
            """,
            """
            ALTER FOREIGN TABLE "campusonline"."stud" DROP COLUMN EMAIL;
            """,
        ),
        (
            """
            CREATE MATERIALIZED VIEW "public"."campusonline_student" AS SELECT
                stud_nr::integer AS id,
                stud_mnr AS matriculation,
                stud_famnam AS last_name,
                stud_vorname AS first_name,
                stud_akadgrad AS title,
                stud_mifare AS cardid,
                stud_benutzername AS username,
                pers_profilbild AS avatar,
                email
            FROM "campusonline"."stud"
            WITH DATA;
            """,
            """
            DROP MATERIALIZED VIEW IF EXISTS "public"."campusonline_student";
            """,
        ),
        (
            """
            CREATE INDEX campusonline_student_id_idx ON "public"."campusonline_student" ("id");
            """,
            """
            DROP INDEX IF EXISTS campusonline_student_id_idx;
            """,
        ),
        (
            """
            CREATE INDEX campusonline_student_matriculation_idx ON "public"."campusonline_student" ("matriculation");
            """,
            """
            DROP INDEX IF EXISTS campusonline_student_matriculation_idx;
            """,
        ),
        (
            """
            CREATE INDEX campusonline_student_cardid_idx ON "public"."campusonline_student" ("cardid");
            """,
            """
            DROP INDEX IF EXISTS campusonline_student_cardid_idx;
            """,
        ),
        (
            """
            CREATE INDEX campusonline_student_username_idx ON "public"."campusonline_student" ("username");
            """,
            """
            DROP INDEX IF EXISTS campusonline_student_username_idx;
            """,
        ),
        (
            """
            CREATE INDEX campusonline_student_email_idx ON "public"."campusonline_student" ("email");
            """,
            """
            DROP INDEX IF EXISTS campusonline_student_email_idx;
            """,
        ),
    ]

    dependencies = [
        ("campusonline", "0057_organization_leave"),
    ]

    operations = [
        migrations.RunSQL(
            [forward for forward, reverse in ops],
            [reverse for forward, reverse in reversed(ops)],
        )
    ]
