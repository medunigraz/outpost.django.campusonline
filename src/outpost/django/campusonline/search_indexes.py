from celery_haystack.indexes import CelerySearchIndex
from haystack import indexes

from . import models


class BulletinPageIndex(CelerySearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    issue = indexes.CharField(model_attr="bulletin__issue")
    academic_year = indexes.CharField(model_attr="bulletin__academic_year")

    def get_model(self):
        return models.BulletinPage

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class PersonIndex(CelerySearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    presentation = indexes.CharField(use_template=True)
    autocomplete = indexes.EdgeNgramField(use_template=True)

    def get_model(self):
        return models.Person

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class StudentIndex(CelerySearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    presentation = indexes.CharField(use_template=True)
    autocomplete = indexes.EdgeNgramField(use_template=True)

    def get_model(self):
        return models.Student

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class RoomIndex(CelerySearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    presentation = indexes.CharField(use_template=True)
    autocomplete = indexes.EdgeNgramField(use_template=True)

    def get_model(self):
        return models.Room

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
