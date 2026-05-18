from django.urls import reverse
from drf_haystack.serializers import HaystackSerializerMixin
from phonenumbers import (
    PhoneNumberFormat,
    format_number,
)
from phonenumbers import parse as parse_number
from phonenumbers import phonenumberutil
from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework.serializers import (
    ModelSerializer,
    PrimaryKeyRelatedField,
    SerializerMethodField,
)

from . import models
from .conf import settings


class RoomCategorySerializer(ModelSerializer):
    class Meta:
        model = models.RoomCategory
        fields = "__all__"


class FloorSerializer(ModelSerializer):
    class Meta:
        model = models.Floor
        exclude = ("short",)


class BuildingSerializer(ModelSerializer):
    class Meta:
        model = models.Building
        fields = "__all__"


class RoomSerializer(ModelSerializer):
    category = RoomCategorySerializer()
    floor = FloorSerializer()
    building = BuildingSerializer()

    class Meta:
        model = models.Room
        fields = (
            "id",
            "category",
            "floor",
            "building",
            "title",
            "name_short",
            "name_full",
            "organization",
            "geo",
        )


class FunctionSerializer(FlexFieldsModelSerializer):
    """
    ## Expansions

    To activate relation expansion add the desired fields as a comma separated
    list to the `expand` query parameter like this:

        ?expand=<field>,<field>,<field>,...

    The following relational fields can be expanded:

     * `persons`

    """

    @property
    def expandable_fields(self):
        serializer = "PersonSerializer"
        request = self.context.get("request", None)
        if request:
            if request.user:
                if request.user.is_authenticated:
                    serializer = "AuthenticatedPersonSerializer"
        return {
            "persons": (
                f"{self.__class__.__module__}.{serializer}",
                {"source": "persons", "many": True},
            )
        }

    class Meta:
        model = models.Function
        fields = "__all__"


class OrganizationTypeSerializer(ModelSerializer):
    class Meta:
        model = models.OrganizationType
        fields = "__all__"


class OrganizationSerializer(FlexFieldsModelSerializer):
    """
    ## Expansions

    To activate relation expansion add the desired fields as a comma separated
    list to the `expand` query parameter like this:

        ?expand=<field>,<field>,<field>,...

    The following relational fields can be expanded:

     * `parent`
     * `persons` <i class="glyphicon glyphicon-lock"></i>
     * `persons_leave` <i class="glyphicon glyphicon-lock"></i>
     * `publication_authorship`
     * `type`

    """

    @property
    def expandable_fields(self):
        return {
            "publication_authorship": (
                "outpost.django.research.serializers.PublicationOrganizationSerializer",
                {"source": "publication_authorship", "many": True},
            ),
            "parent": (
                f"{self.__class__.__module__}.{self.__class__.__name__}",
                {"source": "parent", "many": False},
            ),
            "type": (
                f"{self.__class__.__module__}.OrganizationTypeSerializer",
                {"source": "type", "many": False},
            ),
        }

    class Meta:
        model = models.Organization
        fields = (
            "id",
            "name",
            "short",
            "sib_order",
            "category",
            "address",
            "email",
            "phone",
            "url",
            "parent",
            "fax",
            "office",
            "publication_authorship",
            "type",
            "university_law",
        )


class AuthenticatedOrganizationSerializer(OrganizationSerializer):
    persons = PrimaryKeyRelatedField(many=True, read_only=True)

    @property
    def expandable_fields(self):
        return {
            **super().expandable_fields,
            **{
                "parent": (
                    f"{self.__class__.__module__}.{self.__class__.__name__}",
                    {"source": "parent", "many": False},
                ),
                "persons": (
                    f"{self.__class__.__module__}.AuthenticatedPersonSerializer",
                    {"source": "persons", "many": True},
                ),
                "persons_leave": (
                    f"{self.__class__.__module__}.AuthenticatedPersonSerializer",
                    {"source": "persons_leave", "many": True},
                ),
            },
        }

    class Meta(OrganizationSerializer.Meta):
        fields = OrganizationSerializer.Meta.fields + ("persons", "persons_leave")


class PersonSerializer(FlexFieldsModelSerializer):
    """
    ## Expansions

    To activate relation expansion add the desired fields as a comma separated
    list to the `expand` query parameter like this:

        ?expand=<field>,<field>,<field>,...

    The following relational fields can be expanded:

     * `functions` <i class="glyphicon glyphicon-lock"></i>
     * `organizations` <i class="glyphicon glyphicon-lock"></i>
     * `organizations_leave` <i class="glyphicon glyphicon-lock"></i>
     * `classification`
     * `expertise`
     * `knowledge`
     * `education`

    """

    room = RoomSerializer()

    expandable_fields = {
        "classifications": (
            "outpost.django.research.serializers.ClassificationSerializer",
            {"source": "classifications", "many": True},
        ),
        "expertise": (
            "outpost.django.research.serializers.ExpertiseSerializer",
            {"source": "expertise", "many": True},
        ),
        "knowledge": (
            "outpost.django.research.serializers.KnowledgeSerializer",
            {"source": "knowledge", "many": True},
        ),
        "education": (
            "outpost.django.research.serializers.EducationSerializer",
            {"source": "education", "many": True},
        ),
    }

    class Meta:
        model = models.Person
        fields = (
            "id",
            "room",
            "avatar",
            "card",
            "first_name",
            "last_name",
            "title",
            "consultation",
            "appendix",
            "phone",
            "phone_external",
            "fax",
            "card",
            "classifications",
            "expertise",
            "knowledge",
            "education",
            "academic_title",
            "miscellaneous_title",
            "official_title",
        )


class AuthenticatedPersonSerializer(PersonSerializer):
    avatar = SerializerMethodField()
    mobile = SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request", None)
        if request is not None:
            # TODO: Handle special fields only available with certain permissions.
            pass

    @property
    def expandable_fields(self):
        return {
            **super().expandable_fields,
            **{
                "functions": (
                    f"{self.__class__.__module__}.FunctionSerializer",
                    {"source": "functions", "many": True},
                ),
                "organizations": (
                    f"{self.__class__.__module__}.OrganizationSerializer",
                    {"source": "organizations", "many": True},
                ),
                "organizations_leave": (
                    f"{self.__class__.__module__}.OrganizationSerializer",
                    {"source": "organizations_leave", "many": True},
                ),
            },
        }

    class Meta(PersonSerializer.Meta):
        fields = PersonSerializer.Meta.fields + (
            "email",
            "sex",
            "mobile",
            "functions",
            "organizations",
            "organizations_leave",
            "employed",
        )

    def get_avatar(self, obj):
        if not obj.avatar_private:
            return None
        path = reverse("campusonline:avatar-private", kwargs={"hash": obj.hash})
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(path)
        return path

    def get_mobile(self, obj):
        try:
            p = parse_number(obj.mobile, settings.CAMPUSONLINE_PHONE_NUMBER_REGION)
            return format_number(p, PhoneNumberFormat.INTERNATIONAL)
        except phonenumberutil.NumberParseException:
            return None


class ExternalSerializer(ModelSerializer):
    """"""

    class Meta:
        model = models.External
        fields = ("id", "first_name", "last_name", "title")


class PersonOrganizationFunctionSerializer(ModelSerializer):
    person = PersonSerializer()
    organization = OrganizationSerializer()
    function = FunctionSerializer()

    class Meta:
        model = models.PersonOrganizationFunction
        fields = "__all__"


class DistributionListSerializer(FlexFieldsModelSerializer):
    """
    ## Expansions

    To activate relation expansion add the desired fields as a comma separated
    list to the `expand` query parameter like this:

        ?expand=<field>,<field>,<field>,...

    The following relational fields can be expanded:

     * `persons`
     * `students`

    """

    @property
    def expandable_fields(self):
        person = "PersonSerializer"
        request = self.context.get("request", None)
        if request:
            if request.user:
                if request.user.is_authenticated:
                    person = "AuthenticatedPersonSerializer"
        return {
            "persons": (
                f"{self.__class__.__module__}.{person}",
                {"source": "persons", "many": True},
            ),
            "students": (
                f"{self.__class__.__module__}.StudentSerializer",
                {"source": "students", "many": True},
            ),
        }

    class Meta:
        model = models.DistributionList
        fields = "__all__"


class StudentSerializer(ModelSerializer):
    class Meta:
        model = models.Student
        fields = ("id", "first_name", "last_name", "title", "avatar")


class AuthenticatedStudentSerializer(StudentSerializer):
    class Meta(StudentSerializer.Meta):
        fields = StudentSerializer.Meta.fields + (
            "email",
            "immunized",
        )


class CourseSerializer(ModelSerializer):
    class Meta:
        model = models.Course
        fields = ("id", "name", "category", "year", "semester")


class CourseGroupSerializer(ModelSerializer):
    course = CourseSerializer()

    class Meta:
        model = models.CourseGroup
        fields = ("id", "course", "name")


class CourseGroupTermSerializer(ModelSerializer):
    coursegroup = CourseGroupSerializer()
    person = PersonSerializer()
    room = RoomSerializer()

    class Meta:
        model = models.CourseGroupTerm
        fields = (
            "id",
            "coursegroup",
            "person",
            "start",
            "end",
            "room",
            "title",
            "term",
        )


class EventSerializer(ModelSerializer):
    building = BuildingSerializer()
    room = RoomSerializer()
    course = CourseSerializer()

    class Meta:
        model = models.Event
        fields = "__all__"


class BulletinSerializer(ModelSerializer):
    class Meta:
        model = models.Bulletin
        fields = "__all__"


class BulletinPageSerializer(ModelSerializer):
    bulletin = BulletinSerializer()

    class Meta:
        model = models.BulletinPage
        fields = ("bulletin", "index", "text")


class BulletinPageSearchSerializer(HaystackSerializerMixin, BulletinPageSerializer):
    class Meta(BulletinPageSerializer.Meta):
        search_fields = ("text",)


class FinalThesisSerializer(FlexFieldsModelSerializer):
    """
    ## Expansions

    To activate relation expansion add the desired fields as a comma separated
    list to the `expand` query parameter like this:

        ?expand=<field>,<field>,<field>,...

    The following relational fields can be expanded:

     * `author`
     * `tutor`
     * `organization`

    """

    @property
    def expandable_fields(self):
        serializer = "PersonSerializer"
        request = self.context.get("request", None)
        if request:
            if request.user:
                if request.user.is_authenticated:
                    serializer = "AuthenticatedPersonSerializer"
        return {
            "author": (f"{__name__}.StudentSerializer", {"source": "author"}),
            "tutor": (f"{__name__}.{serializer}", {"source": "tutor"}),
            "organization": (
                f"{__name__}.OrganizationSerializer",
                {"source": "organization"},
            ),
        }

    class Meta:
        model = models.FinalThesis
        fields = "__all__"


class CountrySerializer(ModelSerializer):
    """"""

    class Meta:
        model = models.Country
        fields = "__all__"


class ExamModeSerializer(ModelSerializer):
    """"""

    class Meta:
        model = models.ExamMode
        fields = "__all__"


class ExamTypeSerializer(ModelSerializer):
    """"""

    class Meta:
        model = models.ExamType
        fields = "__all__"


class ExamSerializer(FlexFieldsModelSerializer):
    """
    ## Expansions

    To activate relation expansion add the desired fields as a comma separated
    list to the `expand` query parameter like this:

        ?expand=<field>,<field>,<field>,...

    The following relational fields can be expanded:

     * `organization`
     * `mode`
     * `type`
     * `examiner`
     * `course`

    """

    @property
    def expandable_fields(self):
        serializer = "PersonSerializer"
        request = self.context.get("request", None)
        if request:
            if request.user:
                if request.user.is_authenticated:
                    serializer = "AuthenticatedPersonSerializer"
        return {
            "organization": (
                f"{__name__}.OrganizationSerializer",
                {"source": "organization"},
            ),
            "modes": (f"{__name__}.ExamModeSerializer", {"source": "mode"}),
            "type": (f"{__name__}.ExamTypeSerializer", {"source": "type"}),
            "examiner": (f"{__name__}.{serializer}", {"source": "examiner"}),
            "course": (f"{__name__}.CourseSerializer", {"source": "course"}),
        }

    class Meta:
        model = models.Exam
        fields = "__all__"


class ExamineeStatusSerializer(ModelSerializer):
    """"""

    class Meta:
        model = models.ExamineeStatus
        fields = "__all__"


class ExamineeSerializer(FlexFieldsModelSerializer):
    """
    ## Expansions

    To activate relation expansion add the desired fields as a comma separated
    list to the `expand` query parameter like this:

        ?expand=<field>,<field>,<field>,...

    The following relational fields can be expanded:

     * `exam`
     * `student`
     * `status`

    """

    @property
    def expandable_fields(self):
        return {
            "exam": (f"{__name__}.ExamSerializer", {"source": "exam"}),
            "student": (f"{__name__}.StudentSerializer", {"source": "student"}),
            "status": (f"{__name__}.ExamineeStatusSerializer", {"source": "status"}),
        }

    class Meta:
        model = models.Examinee
        fields = "__all__"


class ScienceBranchSerializer(FlexFieldsModelSerializer):
    """
    ## Expansions

    To activate relation expansion add the desired fields as a comma separated
    list to the `expand` query parameter like this:

        ?expand=<field>,<field>,<field>,...

    The following relational fields can be expanded:

     * `parent`

    """

    @property
    def expandable_fields(self):
        return {
            "parent": (
                f"{self.__class__.__module__}.{self.__class__.__name__}",
                {"source": "parent", "many": False},
            ),
        }

    class Meta:
        model = models.ScienceBranch
        fields = "__all__"
