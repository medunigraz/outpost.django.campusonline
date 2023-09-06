import logging
from datetime import timedelta

from celery import shared_task
from django.core.cache import (
    cache,
    caches,
)
from django.core.cache.backends.base import InvalidCacheBackendError
from django.db import connection
from django.utils.translation import gettext_lazy as _
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig

from .conf import settings
from .models import (
    Person,
    Student,
)
from .schema import linz

logger = logging.getLogger(__name__)


class SynchronizationTasks:
    @shared_task(
        bind=True, ignore_result=True, name=f"{__name__}.Synchronization:usernames"
    )
    def usernames(task):
        logger.info("Updating username redis cache")
        try:
            cache = caches["meduniverse"]
        except InvalidCacheBackendError:
            logger.info("No meduniverse cache defined, not running")
            return

        persons = Person.objects.all()
        for p in persons:
            cache.set(f"{p.__class__.__name__}:username:{p.username}", p.pk)
            cache.set(f"{p.__class__.__name__}:id:{p.pk}", p.username)

        students = Student.objects.all()
        for s in students:
            cache.set(f"{s.__class__.__name__}:username:{s.username}", s.pk)
            cache.set(f"{s.__class__.__name__}:id:{s.pk}", s.username)


class XMLTasks:
    @shared_task(bind=True, ignore_result=True, name=f"{__name__}.XML:hydrate")
    def hydrate(task):
        def columns(cursor):
            return next(zip(*cursor.description))

        def fetchdict(cursor):
            columns = [col.name for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

        def conditions(keys):
            return " AND ".join(["{name}=%s".format(name=name) for name in keys])

        root = linz.Exchange()

        keys_FACH = set(
            (
                "SKZ_UNI",
                "SKZ_KEY",
                "SKZKEY",
                "VERSION",
                "ABSCHNITT",
            )
        )

        keys_GHK = keys_FACH | set(("KENNUNG",))

        with connection.cursor() as cursor_STPL:
            cursor_STPL.execute("SELECT * FROM linz.stpl")
            for row_STPL in fetchdict(cursor_STPL):
                STPL = linz.StplType()
                for name in columns(cursor_STPL):
                    if hasattr(STPL, name) and row_STPL[name]:
                        setattr(STPL, name, row_STPL[name])
                with connection.cursor() as cursor_FACH:
                    sql = "SELECT * FROM linz.fach WHERE {cond}".format(
                        cond=conditions(keys_FACH)
                    )
                    cursor_FACH.execute(
                        sql, [row_STPL[key.lower()] for key in keys_FACH]
                    )
                    for row_FACH in fetchdict(cursor_FACH):
                        FACH = linz.FachType()
                        for name in set(columns(cursor_FACH)) - keys_FACH:
                            if hasattr(FACH, name) and row_FACH[name]:
                                setattr(FACH, name, row_FACH[name])
                        with connection.cursor() as cursor_GHK:
                            sql = "SELECT * FROM linz.ghk WHERE {cond}".format(
                                cond=conditions(keys_GHK)
                            )
                            cursor_GHK.execute(
                                sql, [row_FACH[key.lower()] for key in keys_GHK]
                            )
                            for row_GHK in fetchdict(cursor_GHK):
                                GHK = linz.GhkType()
                                for name in set(columns(cursor_GHK)) - keys_GHK:
                                    if hasattr(GHK, name) and row_GHK[name]:
                                        setattr(GHK, name, row_GHK[name])
                                FACH.ghk.append(GHK)
                        STPL.fach.append(FACH)
                root.stpl.append(STPL)

            with connection.cursor() as cursor_LV:
                cursor_LV.execute("SELECT * FROM linz.lv")
                for row_LV in fetchdict(cursor_LV):
                    LV = linz.LvType()
                    for name in columns(cursor_LV):
                        if hasattr(LV, name) and row_LV[name]:
                            setattr(LV, name, row_LV[name])
                    root.lv.append(LV)

            with connection.cursor() as cursor_PV:
                cursor_PV.execute("SELECT * FROM linz.pv")
                for row_PV in fetchdict(cursor_PV):
                    PV = linz.PvType()
                    for name in columns(cursor_PV):
                        if hasattr(PV, name) and row_PV[name]:
                            setattr(PV, name, row_PV[name])
                    root.pv.append(PV)

        config = SerializerConfig(pretty_print=True)
        serializer = XmlSerializer(config=config)
        body = serializer.render(root, ns_map={None: linz.__NAMESPACE__})
        cache.set(settings.CAMPUSONLINE_XML_CACHE_KEY, body)
        logging.info(f"Finished generating new XML body with size {len(body)}")
        return body
