import logging
from datetime import timedelta

from celery.task import PeriodicTask
from django.core.cache import caches
from django.core.cache.backends.base import InvalidCacheBackendError

from .models import Person, Student

logger = logging.getLogger(__name__)


class UsernameSyncTask(PeriodicTask):
    run_every = timedelta(minutes=5)

    def run(self, **kwargs):
        logger.info("Updating username redis cache")
        try:
            cache = caches["meduniverse"]
        except InvalidCacheBackendError:
            logger.info("No meduniverse cache defined, not running UsernameSyncTask")
            return

        persons = Person.objects.all()
        for p in persons:
            cache.set(f"{p.__class__.__name__}:username:{p.username}", p.pk)
            cache.set(f"{p.__class__.__name__}:id:{p.pk}", p.username)

        students = Student.objects.all()
        for s in students:
            cache.set(f"{s.__class__.__name__}:username:{s.username}", s.pk)
            cache.set(f"{s.__class__.__name__}:id:{s.pk}", s.username)
