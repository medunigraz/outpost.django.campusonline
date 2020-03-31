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
        id_to_username = {}
        username_to_id = {}

        persons = Person.objects.all()
        id_to_username.update({p.pk: p.username for p in persons})
        username_to_id.update({p.username: p.pk for p in persons})
        for p in persons:
            cache.set(f"username:{p.username}", p.pk)
            cache.set(f"id:{p.pk}", p.username)

        students = Student.objects.all()
        id_to_username.update({s.pk: s.username for s in students})
        username_to_id.update({s.username: s.pk for s in students})
        for s in students:
            cache.set(f"username:{s.username}", s.pk)
            cache.set(f"id:{s.pk}", s.username)

        cache.set("id_to_username", id_to_username)
        cache.set("username_to_id", username_to_id)
