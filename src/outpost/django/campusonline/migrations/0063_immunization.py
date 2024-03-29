# Generated by Django 2.2.26 on 2022-05-11 08:36

from django.db import migrations


class Migration(migrations.Migration):

    ops = [
        (
            """
            ALTER FOREIGN TABLE "campusonline"."stud_impfstatus" ADD COLUMN COVID_IMUNISIERUNGS_STATUS varchar;
            """,
            """
            ALTER FOREIGN TABLE "campusonline"."stud_impfstatus" DROP COLUMN COVID_IMUNISIERUNGS_STATUS;
            """,
        ),
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
                s.stud_nr::integer AS id,
                s.stud_mnr AS matriculation,
                s.stud_famnam AS last_name,
                s.stud_vorname AS first_name,
                s.stud_akadgrad AS title,
                s.stud_mifare AS cardid,
                s.stud_benutzername AS username,
                s.pers_profilbild AS avatar,
                s.email,
                UPPER(coalesce(si.impfung_erhalten, 'NEIN')) = 'JA' AS immunized
            FROM campusonline.stud s
                LEFT JOIN
                    campusonline.stud_impfstatus si on s.stud_nr::int = si.st_person_nr::int
            WITH DATA;
            """,
        ),
        (
            """
            CREATE MATERIALIZED VIEW "public"."campusonline_student" AS SELECT
                s.stud_nr::integer AS id,
                s.stud_mnr AS matriculation,
                s.stud_famnam AS last_name,
                s.stud_vorname AS first_name,
                s.stud_akadgrad AS title,
                s.stud_mifare AS cardid,
                s.stud_benutzername AS username,
                s.pers_profilbild AS avatar,
                s.email,
                UPPER(coalesce(si.covid_imunisierungs_status, 'N')) = 'J' AS immunized
            FROM campusonline.stud s
                LEFT JOIN
                    campusonline.stud_impfstatus si on s.stud_nr::int = si.st_person_nr::int
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
        (
            """
            ALTER FOREIGN TABLE "campusonline"."stud_impfstatus" DROP COLUMN IMPFUNG_ERHALTEN;
            """,
            """
            ALTER FOREIGN TABLE "campusonline"."stud_impfstatus" ADD COLUMN IMPFUNG_ERHALTEN varchar;
            """,
        ),
        (
            """
            ALTER FOREIGN TABLE "campusonline"."stud_impfstatus" DROP COLUMN STATUS;
            """,
            """
            ALTER FOREIGN TABLE "campusonline"."stud_impfstatus" ADD COLUMN STATUS varchar;
            """,
        ),
    ]

    dependencies = [
        ("campusonline", "0062_finalthesis_extended"),
    ]

    operations = [
        migrations.RunSQL(
            [forward for forward, reverse in ops],
            [reverse for forward, reverse in reversed(ops)],
        )
    ]
