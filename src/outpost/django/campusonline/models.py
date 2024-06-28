import logging
from io import BytesIO
from locale import (
    LC_ALL,
    LC_CTYPE,
    LC_NUMERIC,
)
from typing import Optional

import django
import requests
from django.contrib.gis.db import models
from django.contrib.postgres.fields import HStoreField
from django.utils.translation import gettext_lazy as _
from ordered_model.models import OrderedModel
from outpost.django.base.decorators import locale
from outpost.django.base.models import RelatedManager
from outpost.django.base.signals import materialized_view_refreshed
from outpost.django.base.tasks import MaterializedViewTasks
from PIL import Image
from popplerqt5 import Poppler
from PyQt5.QtCore import (
    QBuffer,
    QIODevice,
    QRectF,
)
from treebeard.al_tree import AL_Node

from .conf import settings

logger = logging.getLogger(__name__)


class RoomCategory(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "campusonline_room_category"
        ordering = ("name",)

    class Refresh:
        interval = 86400

    def __str__(self):
        return self.name


class Room(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=256, blank=True, null=True)
    building = models.ForeignKey(
        "Building",
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
        related_name="+",
    )
    floor = models.ForeignKey(
        "Floor",
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
        related_name="+",
    )
    name_short = models.CharField(max_length=256, blank=True, null=True)
    name_full = models.CharField(max_length=256, blank=True, null=True)
    area = models.DecimalField(
        max_digits=65535, decimal_places=1, blank=True, null=True
    )
    height = models.DecimalField(
        max_digits=65535, decimal_places=1, blank=True, null=True
    )
    organization = models.ForeignKey(
        "Organization",
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
        related_name="+",
    )
    category = models.ForeignKey(
        "RoomCategory",
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
        related_name="+",
    )

    class Meta:
        managed = False
        db_table = "campusonline_room"
        ordering = ("name_full", "title")

    class Refresh:
        interval = 7200

    def __str__(self):
        return "{s.name_full}: {s.title}".format(s=self)


class Floor(models.Model):
    id = models.IntegerField(primary_key=True)
    short = models.CharField(max_length=64, blank=True, null=True)
    name = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "campusonline_floor"
        ordering = ("name",)

    class Refresh:
        interval = 86400

    def __str__(self):
        return "{s.name} ({s.short})".format(s=self)


class Building(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=256, blank=True, null=True)
    short = models.CharField(max_length=64, blank=True, null=True)
    address = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "campusonline_building"
        ordering = ("name",)

    class Refresh:
        interval = 86400

    def __str__(self):
        return "{s.name} ({s.short})".format(s=self)


class Function(models.Model):
    """
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`string`)
    Gender neutral name of function.

    ### `name_female` (`string`)
    Female name of function.

    ### `name_male` (`string`)
    Male name of function.

    ### `category` (`string`)
    Type of function with possible values:

     * `fachliche` (Technical)
     * `rechtliche` (Legal)

    ### `leader` (`boolean`)
    Indicate if function is associated with leadership.

    ### `persons` (`[integer]`)
    List of foreign keys to [CAMPUSonline persons](../person) associated with this function.
    """

    CATEGORY_CHOICES = (("fachliche", _("Technical")), ("rechtliche", _("Legal")))

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=256, blank=True, null=True)
    name_female = models.CharField(max_length=256, blank=True, null=True)
    name_male = models.CharField(max_length=256, blank=True, null=True)
    category = models.CharField(
        choices=CATEGORY_CHOICES, max_length=32, blank=True, null=True
    )
    leader = models.BooleanField(null=False)
    persons = models.ManyToManyField("Person", through="PersonOrganizationFunction")

    class Meta:
        managed = False
        db_table = "campusonline_function"
        ordering = ("name", "category")

    class Refresh:
        interval = 86400

    def __str__(s):
        return f"{s.name} ({s.category})"


class Organization(AL_Node):
    """
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`string`)
    Name of organization.

    ### `short` (`string`)
    Short name of organization.

    ### `parent` (`integer`)
    Foreign key to parent [CAMPUSonline organization](../organization). A value
    of `null` inidcated the root organization.

    Only required when assembling the organizational
    [AL tree](https://en.wikipedia.org/wiki/Adjacency_list).

    ### `sib_order` (`integer`)
    Value to sort by.

    Only required when assembling the organizational
    [AL tree](https://en.wikipedia.org/wiki/Adjacency_list).

    ### `category` (`string`)
    Type of organization with possible values:

     * `OE` (Organizational Unit)
     * `FE` (Research Unit)
     * `TE` (Teaching Unit)
     * `V` (Virtual)

    ### `address` (`string`)
    Official post address of organization.

    ### `email` (`string`)
    Official email address of organization.

    ### `phone` (`string`)
    Official phone number of organization.

    ### `fax` (`string`)
    Official fax number of organization.

    ### `url` (`string`)
    Official website URL of organization.

    ### `office` (`string`)
    Free-form text information about the office of this organization.

    ### `persons` (`[integer]`)
    List of foreign keys to [CAMPUSonline persons](../person) that are
    associated with this organization.
    """

    CATEGORY_CHOICES = (
        ("OE", _("Organizational Unit")),
        ("FE", _("Research Unit")),
        ("TE", _("Teaching Unit")),
        ("V", _("Virtual")),
    )

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=256, blank=True, null=True)
    short = models.CharField(max_length=32, blank=True, null=True)
    parent = models.ForeignKey(
        "self",
        models.SET_NULL,
        related_name="children_set",
        db_constraint=False,
        db_index=False,
        null=True,
        blank=True,
    )
    sib_order = models.PositiveIntegerField()
    category = models.CharField(
        choices=CATEGORY_CHOICES, max_length=32, blank=True, null=True
    )
    address = models.TextField(blank=True, null=True)
    email = models.CharField(max_length=256, blank=True, null=True)
    phone = models.CharField(max_length=256, blank=True, null=True)
    fax = models.CharField(max_length=256, blank=True, null=True)
    url = models.CharField(max_length=256, blank=True, null=True)
    office = models.TextField(blank=True, null=True)
    type = models.ForeignKey(
        "OrganizationType",
        models.DO_NOTHING,
        related_name="organizations",
        db_constraint=False,
        db_index=False,
        null=True,
        blank=True,
    )
    university_law = models.BooleanField()

    class Meta:
        managed = False
        db_table = "campusonline_organization"
        ordering = ("name",)

    class Refresh:
        interval = 7200

    def __str__(self):
        return self.name


class OrganizationType(models.Model):
    name = models.TextField(max_length=256)
    short = models.CharField(max_length=128, null=True, blank=True)

    class Meta:
        managed = False
        db_table = "campusonline_organization_type"
        ordering = ("name",)

    class Refresh:
        interval = 86400

    def __str__(self):
        return self.name


class Person(models.Model):
    """
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `first_name` (`string`)
    First name of person.

    ### `last_name` (`string`)
    Last name of person.

    ### `title` (`string`)
    Titles bestowed onto the person.

    ### `email` (`string`) <i class="glyphicon glyphicon-lock"></i>
    Email address (*only visible when authenticated*).

    ### `room` (`integer`)
    Foreign key to [CAMPUSonline room](../room) where this person has their primary workplace.

    ### `card` (`string`)
    URL to CAMPUSonline business card.

    ### `sex` (`string`)
    Sex of person:

     * `W` (Female)
     * `M` (Male)

    ### `consultation` (`string`)
    Consultation hours as free form text. Content may contain other information.

    ### `appendix` (`string`)
    Miscellaneous information about person as free form text.

    ### `avatar` (`string`)
    URL to user avatar picture. May point to an empty image.

    ### `phone` (`string`)
    Office phone number of person.

    ### `phone_external` (`string`)
    External phone number of person.

    ### `fax` (`string`)
    Office fax number of person.

    ### `functions` (`[integer]`) <i class="glyphicon glyphicon-lock"></i>
    List of foreign keys to [CAMPUSonline functions](../function) this person carries.

    ### `organizations` (`[integer]`) <i class="glyphicon glyphicon-lock"></i>
    List of foreign keys to [CAMPUSonline organizations](../organization) where this person is currently active.

    ### `organizations_leave` (`[integer]`) <i class="glyphicon glyphicon-lock"></i>
    List of foreign keys to [CAMPUSonline organizations](../organization) where this person is currently on leave.
    """

    GENDER_CHOICES = (
        ("W", _("Female")),
        ("M", _("Male")),
        ("X", _("Divers")),
        ("U", _("Unknown")),
        ("O", _("Open")),
        ("I", _("Inter")),
        ("K", _("No record")),
    )

    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=256, blank=True, null=True)
    last_name = models.CharField(max_length=256, blank=True, null=True)
    title = models.CharField(max_length=256, blank=True, null=True)
    email = models.EmailField()
    room = models.ForeignKey(
        "Room",
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
        related_name="+",
    )
    sex = models.CharField(choices=GENDER_CHOICES, max_length=1, blank=True, null=True)
    username = models.CharField(max_length=256, blank=True, null=True)
    consultation = models.TextField(blank=True, null=True)
    appendix = models.TextField(blank=True, null=True)
    avatar = models.URLField(blank=True, null=True)
    card = models.URLField(blank=True, null=True)
    functions = models.ManyToManyField("Function", through="PersonOrganizationFunction")
    organizations = models.ManyToManyField(
        "Organization",
        db_table="campusonline_person_organization",
        db_constraint=False,
        related_name="persons",
    )
    organizations_leave = models.ManyToManyField(
        "Organization",
        db_table="campusonline_person_organization_leave",
        db_constraint=False,
        related_name="persons_leave",
    )
    avatar_private = models.BinaryField()
    hash = models.CharField(max_length=64)
    phone = models.CharField(max_length=256, blank=True, null=True)
    mobile = models.CharField(max_length=256, blank=True, null=True)
    employed = models.BooleanField()
    card = models.URLField(blank=True, null=True)
    fax = models.CharField(max_length=256, blank=True, null=True)
    phone_external = models.CharField(max_length=256, blank=True, null=True)
    academic_title = HStoreField()
    miscellaneous_title = HStoreField()
    official_title = HStoreField()

    class Meta:
        managed = False
        db_table = "campusonline_person"
        ordering = ("last_name", "first_name")

    class Refresh:
        interval = 1800

    def __str__(self):
        return "{s.last_name}, {s.first_name}".format(s=self)


class External(models.Model):
    """
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `first_name` (`string`)
    First name of person.

    ### `last_name` (`string`)
    Last name of person.

    ### `title` (`string`)
    Titles bestowed onto the person.

    ### `sex` (`string`)
    Sex of person:

     * `W` (Female)
     * `M` (Male)
    """

    GENDER_CHOICES = (("W", _("Female")), ("M", _("Male")))

    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=256, blank=True, null=True)
    last_name = models.CharField(max_length=256, blank=True, null=True)
    title = models.CharField(max_length=256, blank=True, null=True)
    sex = models.CharField(choices=GENDER_CHOICES, max_length=1, blank=True, null=True)
    username = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "campusonline_external"
        ordering = ("last_name", "first_name")

    class Refresh:
        interval = 1800

    def __str__(self):
        return "{s.last_name}, {s.first_name}".format(s=self)


class PersonOrganizationFunction(models.Model):
    id = models.CharField(primary_key=True, max_length=128)
    person = models.ForeignKey(
        "Person",
        models.DO_NOTHING,
        db_constraint=False,
        null=False,
        blank=False,
        related_name="+",
    )
    organization = models.ForeignKey(
        "Organization",
        models.DO_NOTHING,
        db_constraint=False,
        null=False,
        blank=False,
        related_name="+",
    )
    function = models.ForeignKey(
        "function",
        models.DO_NOTHING,
        db_constraint=False,
        null=False,
        blank=False,
        related_name="+",
    )

    class Meta:
        managed = False
        db_table = "campusonline_personorganizationfunction"
        ordering = ("id",)

    class Refresh:
        interval = 7200

    def __str__(self):
        return "{s.person}, {s.organization}: {s.function}".format(s=self)


class AbstractDistributionList(models.Model):
    id = models.CharField(primary_key=True, max_length=128)
    name = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        ordering = ("name",)
        abstract = True

    def __str__(self):
        return self.name


class DistributionListInternal(AbstractDistributionList):
    persons = models.ManyToManyField(
        "Person", db_constraint=False, related_name="distribution_list_internal"
    )


class DistributionList(AbstractDistributionList):
    """
    ## Fields

    ### `id` (`string`)
    Primary key. May contain alphabetic characters.

    ### `name` (`string`)
    Name of distribtuion list.

    ### `persons` (`[integer]`) <i class="glyphicon glyphicon-lock"></i>
    List of foreign keys to [CAMPUSonline persons](../person) that belong to this distribution list.
    """

    persons = models.ManyToManyField(
        "Person",
        db_table="campusonline_distributionlist_person",
        db_constraint=False,
        related_name="distributionslists",
    )
    students = models.ManyToManyField(
        "Student",
        db_table="campusonline_distributionlist_student",
        db_constraint=False,
        related_name="distributionslists",
    )

    class Meta(AbstractDistributionList.Meta):
        managed = False
        db_table = "campusonline_distributionlist"

    class Refresh:
        interval = 1800


class Student(models.Model):
    id = models.IntegerField(primary_key=True)
    matriculation = models.CharField(max_length=16, blank=True, null=True)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    title = models.CharField(max_length=256, blank=True, null=True)
    cardid = models.CharField(max_length=16, blank=True, null=True)
    username = models.CharField(max_length=256, blank=True, null=True)
    avatar = models.URLField(blank=True, null=True)
    email = models.EmailField()
    immunized = models.BooleanField()

    class Meta:
        managed = False
        db_table = "campusonline_student"
        ordering = ("last_name", "first_name")

    class Refresh:
        interval = 7200

    @property
    def display(self):
        if self.title:
            return "{s.title} {s.first_name} {s.last_name}".format(s=self)
        return "{s.first_name} {s.last_name}".format(s=self)

    def __str__(self):
        return "{s.last_name}, {s.first_name}".format(s=self)


class Course(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=256)
    category = models.CharField(max_length=256)
    year = models.CharField(max_length=256)
    semester = models.CharField(max_length=256)

    class Meta:
        managed = False
        db_table = "campusonline_course"

    class Refresh:
        interval = 86400

    def __str__(self):
        return "{s.name} ({s.semester}:{s.year})".format(s=self)


class CourseGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    course = models.ForeignKey(
        "Course",
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
        related_name="groups",
    )
    name = models.CharField(max_length=256)
    students = models.ManyToManyField("Student")

    class Meta:
        managed = False
        db_table = "campusonline_coursegroup"

    class Refresh:
        interval = 86400

    def __str__(self):
        return "{s.name} ({s.course})".format(s=self)


class CourseGroupTerm(models.Model):
    id = models.CharField(primary_key=True, max_length=128)
    title = models.TextField(null=True)
    coursegroup = models.ForeignKey(
        "CourseGroup", models.DO_NOTHING, db_constraint=False, null=True, blank=True
    )
    person = models.ForeignKey("Person", models.DO_NOTHING, db_constraint=False)
    start = models.DateTimeField()
    end = models.DateTimeField()
    term = models.IntegerField()
    room = models.ForeignKey(
        "Room", models.DO_NOTHING, db_constraint=False, null=True, blank=True
    )

    objects = RelatedManager(
        select=("coursegroup", "coursegroup__course", "person", "room")
    )

    class Meta:
        managed = False
        db_table = "campusonline_coursegroupterm"
        get_latest_by = "start"
        ordering = ("start", "end")
        permissions = (
            (("view_coursegroupterm", _("Can view course group term")),)
            if django.VERSION < (2, 1)
            else tuple()
        )

    class Refresh:
        interval = 86400

    def __str__(s):
        return f"{s.coursegroup} ({s.person}): {s.room} {s.start}-{s.end}"


class Event(OrderedModel):
    """
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `course` (`object`)
    Course this event is associated with.

    ### `category` (`string`)
    Category for this event.

    ### `title` (`string`)
    Title of this event.

    ### `date` (`datetime`)
    Date of event.

    ### `start` (`datetime`)
    Start of event.

    ### `end` (`datetime`)
    End of event.

    ### `building` (`object`)
    Building this event takes place in.

    ### `room` (`object`)
    Building this event takes place in.

    ### `show_end` (`datetime`)
    When to stop showing this event.
    """

    course = models.ForeignKey(
        "Course",
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
        related_name="+",
    )
    category = models.CharField(max_length=256)
    title = models.CharField(max_length=256)
    date = models.DateField()
    start = models.DateTimeField()
    end = models.DateTimeField()
    building = models.ForeignKey(
        "Building",
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
        related_name="+",
    )
    room = models.ForeignKey(
        "Room",
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
        related_name="+",
    )
    show_end = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "campusonline_event"

    class Refresh:
        interval = 3600

    def __str__(self):
        return "{s.category} {s.date}: {s.title} ({s.room})".format(s=self)


class Bulletin(models.Model):
    """
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `academic_year` (`string`)
    The [academic year](https://en.wikipedia.org/wiki/Academic_year) in the
    format of `<winter semester year as 4 digits/summer semster year with two
    digits>`.

    ### `issue` (`string`)
    Issue of bulletin. May contain alphabetical characters.

    ### `published` (`datetime`)
    Date & time when this bulletin was published.

    ### `teaser` (`string`)
    Short teaser for bulletin content.

    ### `url` (`string`)
    URL to [PDF](https://en.wikipedia.org/wiki/PDF) download of bulletin.
    """

    id = models.IntegerField(primary_key=True)
    academic_year = models.CharField(max_length=256)
    issue = models.CharField(max_length=256)
    published = models.DateTimeField()
    teaser = models.TextField()
    url = models.URLField()

    class Meta:
        managed = False
        db_table = "campusonline_bulletin"
        get_latest_by = "published"
        ordering = ("-published",)

    class Refresh:
        interval = 86400

    def __str__(s):
        return f"{s.issue} {s.academic_year} ({s.published})"

    @property
    def content(self) -> Optional[bytes]:
        try:
            req = requests.get(self.url)
            req.raise_for_status()
            return req.content
        except requests.exceptions.RequestException as e:
            logger.warn(f"Could not download bulletin {self}: {e}")
            return None

    def extract(self):
        content = self.content
        if not content:
            return
        doc = Poppler.Document.loadFromData(content)
        if not doc:
            logger.warn(f"Could not parse bulletin {self}")
            return
        for n, p in enumerate(doc):
            bp, created = BulletinPage.objects.get_or_create(
                bulletin=self, index=n, defaults={"bulletin": self, "index": n}
            )
            if created or (bp.harvest and not bp.clean):
                bp.extract(p)
                bp.save()

    @classmethod
    def update(cls, name, model, **kwargs):
        if not cls == model:
            return
        for b in model.objects.all():
            b.extract()


materialized_view_refreshed.connect(
    Bulletin.update, sender=MaterializedViewTasks.refresh
)


class BulletinPage(models.Model):
    bulletin = models.ForeignKey(
        "Bulletin", models.DO_NOTHING, db_constraint=False, related_name="pages"
    )
    index = models.PositiveSmallIntegerField()
    text = models.TextField(null=True)
    clean = models.BooleanField(default=False)
    harvest = models.BooleanField(default=False)

    class Meta:
        ordering = ("-bulletin", "index")
        unique_together = ("bulletin", "index")

    @locale(cat=LC_ALL, loc="C")
    @locale(cat=LC_CTYPE, loc="C")
    @locale(cat=LC_NUMERIC, loc="C")
    def extract(self, page: Poppler.Page):
        from tesserocr import PyTessBaseAPI  # NOQA Stupid assert on LC_* == 'C'

        ocr = PyTessBaseAPI(lang=settings.CAMPUSONLINE_BULLETIN_OCR_LANGUAGE)
        text = page.text(QRectF()).strip()
        if len(text) > settings.CAMPUSONLINE_BULLETIN_OCR_THRESHOLD:
            self.clean = True
            self.text = text
            return
        dpi = settings.CAMPUSONLINE_BULLETIN_OCR_DPI
        buf = QBuffer()
        buf.open(QIODevice.ReadWrite)
        page.renderToImage(dpi, dpi).save(buf, "PNG")
        bio = BytesIO()
        bio.write(buf.data())
        buf.close()
        bio.seek(0)
        img = Image.open(bio)
        ocr.SetImage(img)
        scanned = ocr.GetUTF8Text().strip()
        img.close()
        bio.close()
        self.clean = False
        self.text = scanned


class FinalThesis(models.Model):
    study_designation = models.CharField(max_length=256)
    modified = models.DateTimeField()
    author = models.ForeignKey(
        "Student", models.DO_NOTHING, db_constraint=False, null=True
    )
    author_lastname = models.CharField(max_length=256)
    author_firstname = models.CharField(max_length=256)
    author_title = models.CharField(max_length=256)
    title = HStoreField()
    abstract = HStoreField()
    tutor = models.ForeignKey(
        "Person", models.DO_NOTHING, db_constraint=False, null=True
    )
    tutor_name = models.CharField(max_length=256)
    year = models.PositiveIntegerField()
    url = models.URLField()
    category = models.CharField(max_length=256)
    organization = models.ForeignKey(
        "Organization", models.DO_NOTHING, db_constraint=False, null=True
    )

    class Meta:
        managed = False
        db_table = "campusonline_finalthesis"
        get_latest_by = "modified"
        ordering = ("-modified",)

    def __str__(self):
        return f"{self.author}: {self.title} ({self.year})"


class RoomAllocation(models.Model):
    id = models.CharField(primary_key=True, max_length=128)
    room = models.ForeignKey("Room", models.DO_NOTHING, db_constraint=False)
    term = models.IntegerField()
    student = models.ForeignKey("Student", models.DO_NOTHING, db_constraint=False)
    start = models.DateTimeField()
    end = models.DateTimeField()
    onsite = models.BooleanField()

    class Meta:
        managed = False
        db_table = "campusonline_roomallocation"

    def __str__(self):
        return f"{self.student}: {self.room} ({self.term})"


class Country(models.Model):
    alpha2 = models.CharField(max_length=2, primary_key=True)
    alpha3 = models.CharField(max_length=3)
    name = HStoreField()

    class Meta:
        managed = False
        db_table = "campusonline_country"
        ordering = ("alpha2",)

    def __str__(self):
        return f"{self.alpha2} ({self.alpha3})"


class ExamMode(models.Model):
    short = models.CharField(max_length=8)
    name = HStoreField()

    class Meta:
        managed = False
        db_table = "campusonline_exam_mode"
        ordering = ("short",)

    def __str__(self):
        return self.short


class ExamType(models.Model):
    short = models.CharField(max_length=8)
    name = HStoreField()
    certificate = HStoreField()

    class Meta:
        managed = False
        db_table = "campusonline_exam_type"
        ordering = ("short",)

    def __str__(self):
        return self.short


class Exam(models.Model):
    organization = models.ForeignKey(
        "Organization",
        models.DO_NOTHING,
        db_constraint=False,
        null=False,
        blank=False,
        related_name="+",
    )
    mode = models.ForeignKey(
        "ExamMode",
        models.DO_NOTHING,
        db_constraint=False,
        null=False,
        blank=False,
        related_name="+",
    )
    type = models.ForeignKey(
        "ExamType",
        models.DO_NOTHING,
        db_constraint=False,
        null=False,
        blank=False,
        related_name="+",
    )
    examiner = models.ForeignKey(
        "Person",
        models.DO_NOTHING,
        db_constraint=False,
        null=False,
        blank=False,
        related_name="+",
    )
    course = models.ForeignKey(
        "Course",
        models.DO_NOTHING,
        db_constraint=False,
        null=False,
        blank=False,
        related_name="+",
    )
    registration_start = models.DateTimeField()
    registration_end = models.DateTimeField()
    start = models.DateTimeField()
    online_registration = models.BooleanField()
    note = models.TextField()
    valid = models.BooleanField()
    deregistration_end = models.DateTimeField()
    location = models.TextField()

    class Meta:
        managed = False
        db_table = "campusonline_exam"
        ordering = ("start",)

    def __str__(self):
        return f"{self.type} ({self.mode})"


class ExamineeStatus(models.Model):
    short = models.CharField(max_length=8)
    name = HStoreField()

    class Meta:
        managed = False
        db_table = "campusonline_examinee_status"
        ordering = ("short",)

    def __str__(self):
        return self.short


class Examinee(models.Model):
    exam = models.ForeignKey(
        "Exam",
        models.DO_NOTHING,
        db_constraint=False,
        null=False,
        blank=False,
        related_name="+",
    )
    student = models.ForeignKey(
        "Student",
        models.DO_NOTHING,
        db_constraint=False,
        null=False,
        blank=False,
        related_name="+",
    )
    status = models.ForeignKey(
        "ExamineeStatus",
        models.DO_NOTHING,
        db_constraint=False,
        null=False,
        blank=False,
        related_name="+",
    )
    status_datetime = models.DateTimeField()
    registration = models.DateField()
    assessment_closure = models.DateField()

    class Meta:
        managed = False
        db_table = "campusonline_examinee"
        ordering = ("id",)

    def __str__(self):
        return self.student


class ScienceBranch(AL_Node):
    """
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `code` (`string`)
    Extended code, an expanded form of the primary key.

    ### `level` (`integer`)
    The level (1-4) where this science branch is located.

    ### `name` (`object`)
    A dictionary of names using language as its key.

    ### `short` (`object`)
    A dictionary of short names using language as its key.

    ### `parent` (`integer`)
    Foreign key to parent [CAMPUSonline science branch](../sciencebranch). A value
    of `null` inidcated a root branch.
    """

    code = models.CharField(max_length=32)
    level = models.PositiveSmallIntegerField()
    name = HStoreField()
    short = HStoreField()
    parent = models.ForeignKey(
        "self",
        models.DO_NOTHING,
        related_name="children_set",
        db_constraint=False,
        db_index=False,
        null=True,
        blank=True,
    )
    node_order_by = ("code",)

    class Meta:
        managed = False
        db_table = "campusonline_science_branch"
        ordering = (
            "parent_id",
            "code",
        )

    class Refresh:
        interval = 86400

    def __str__(self):
        return self.code
