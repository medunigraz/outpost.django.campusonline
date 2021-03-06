# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-01-21 07:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    ops = [
        (
            """
            DROP INDEX IF EXISTS campusonline_organization_id_idx;
            """,
            """
            CREATE UNIQUE INDEX campusonline_organization_id_idx ON "public"."campusonline_organization" ("id");
            """,
        ),
        (
            """
            DROP INDEX IF EXISTS campusonline_organization_name_idx;
            """,
            """
            CREATE INDEX campusonline_organization_name_idx ON "public"."campusonline_organization" ("name");
            """,
        ),
        (
            """
            DROP INDEX IF EXISTS campusonline_organization_short_idx;
            """,
            """
            CREATE INDEX campusonline_organization_short_idx ON "public"."campusonline_organization" ("short");
            """,
        ),
        (
            """
            DROP INDEX IF EXISTS campusonline_organization_parent_id_idx;
            """,
            """
            CREATE INDEX campusonline_organization_parent_id_idx ON "public"."campusonline_organization" ("parent_id");
            """,
        ),
        (
            """
            DROP INDEX IF EXISTS campusonline_organization_category_idx;
            """,
            """
            CREATE INDEX campusonline_organization_category_idx ON "public"."campusonline_organization" ("category");
            """,
        ),
        (
            """
            DROP INDEX IF EXISTS campusonline_organization_sib_order_idx;
            """,
            """
            CREATE INDEX campusonline_organization_sib_order_idx ON "public"."campusonline_organization" ("sib_order");
            """,
        ),
        (
            """
            DROP MATERIALIZED VIEW IF EXISTS "public"."campusonline_organization";
            """,
            """
            CREATE MATERIALIZED VIEW "public"."campusonline_organization" AS SELECT
                nr::integer AS id,
                org_name AS name,
                name_kurz AS short,
                basisorganisation::integer AS parent_id,
                sort_hierarchie::integer AS sib_order,
                typ AS category,
                adresse AS address,
                email_adresse AS email,
                telefon_nummer AS phone,
                www_homepage AS url
            FROM "campusonline"."organisationen"
            WITH DATA;
            """,
        ),
        (
            """
            ALTER FOREIGN TABLE "campusonline"."organisationen" ADD COLUMN FAX_NUMMER varchar;
            """,
            """
            ALTER FOREIGN TABLE "campusonline"."organisationen" DROP COLUMN FAX_NUMMER;
            """,
        ),
        (
            """
            ALTER FOREIGN TABLE "campusonline"."organisationen" ADD COLUMN SEKRETARIAT varchar;
            """,
            """
            ALTER FOREIGN TABLE "campusonline"."organisationen" DROP COLUMN SEKRETARIAT;
            """,
        ),
        (
            """
            CREATE MATERIALIZED VIEW "public"."campusonline_organization" AS SELECT
                nr::integer AS id,
                org_name AS name,
                name_kurz AS short,
                basisorganisation::integer AS parent_id,
                sort_hierarchie::integer AS sib_order,
                typ AS category,
                adresse AS address,
                email_adresse AS email,
                telefon_nummer AS phone,
                www_homepage AS url,
                fax_nummer AS fax,
                sekretariat AS office
            FROM "campusonline"."organisationen"
            WITH DATA;
            """,
            """
            DROP MATERIALIZED VIEW IF EXISTS "public"."campusonline_organization";
            """,
        ),
        (
            """
            CREATE UNIQUE INDEX campusonline_organization_id_idx ON "public"."campusonline_organization" ("id");
            """,
            """
            DROP INDEX IF EXISTS campusonline_organization_id_idx;
            """,
        ),
        (
            """
            CREATE INDEX campusonline_organization_name_idx ON "public"."campusonline_organization" ("name");
            """,
            """
            DROP INDEX IF EXISTS campusonline_organization_name_idx;
            """,
        ),
        (
            """
            CREATE INDEX campusonline_organization_short_idx ON "public"."campusonline_organization" ("short");
            """,
            """
            DROP INDEX IF EXISTS campusonline_organization_short_idx;
            """,
        ),
        (
            """
            CREATE INDEX campusonline_organization_parent_id_idx ON "public"."campusonline_organization" ("parent_id");
            """,
            """
            DROP INDEX IF EXISTS campusonline_organization_parent_id_idx;
            """,
        ),
        (
            """
            CREATE INDEX campusonline_organization_category_idx ON "public"."campusonline_organization" ("category");
            """,
            """
            DROP INDEX IF EXISTS campusonline_organization_category_idx;
            """,
        ),
        (
            """
            CREATE INDEX campusonline_organization_sib_order_idx ON "public"."campusonline_organization" ("sib_order");
            """,
            """
            DROP INDEX IF EXISTS campusonline_organization_sib_order_idx;
            """,
        ),
    ]

    dependencies = [("campusonline", "0055_person_numbers")]

    operations = [
        migrations.RunSQL(
            [forward for forward, reverse in ops],
            [reverse for forward, reverse in reversed(ops)],
        )
    ]
