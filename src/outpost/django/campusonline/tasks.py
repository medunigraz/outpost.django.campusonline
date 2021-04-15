import logging
from datetime import timedelta

from celery import shared_task
from django.core.cache import caches
from django.core.cache.backends.base import InvalidCacheBackendError
from django.utils.translation import gettext_lazy as _

from .models import Person, Student

logger = logging.getLogger(__name__)


class SynchronizationTasks:

    @shared_task(bind=True, ignore_result=True, name=f"{__name__}.Synchronization:usernames")
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
