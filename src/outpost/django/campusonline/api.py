from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from drf_haystack.viewsets import HaystackViewSet
from outpost.django.api.permissions import ExtendedDjangoModelPermissions
from outpost.django.base.decorators import docstring_format
from rest_flex_fields.views import FlexFieldsMixin
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_extensions.cache.mixins import CacheResponseMixin

from . import (
    filters,
    key_constructors,
    models,
    serializers,
)

# from rest_framework_extensions.mixins import (
#     CacheResponseAndETAGMixin,
# )
# from rest_framework_extensions.cache.mixins import (
#     CacheResponseMixin,
# )


class RoomCategoryViewSet(CacheResponseMixin, ReadOnlyModelViewSet):
    queryset = models.RoomCategory.objects.all()
    serializer_class = serializers.RoomCategorySerializer
    object_cache_key_func = key_constructors.PersonKeyConstructor()
    list_cache_key_func = key_constructors.PersonKeyConstructor()
    permission_classes = (AllowAny,)


class RoomViewSet(ReadOnlyModelViewSet):
    queryset = models.Room.objects.all()
    serializer_class = serializers.RoomSerializer
    permission_classes = (AllowAny,)
    filter_fields = ("category",)


class FloorViewSet(ReadOnlyModelViewSet):
    queryset = models.Floor.objects.all()
    serializer_class = serializers.FloorSerializer
    permission_classes = (AllowAny,)


class BuildingViewSet(ReadOnlyModelViewSet):
    queryset = models.Building.objects.all()
    serializer_class = serializers.BuildingSerializer
    permission_classes = (AllowAny,)


@docstring_format(
    model=models.Function.__doc__,
    filter=filters.FunctionFilter.__doc__,
    serializer=serializers.FunctionSerializer.__doc__,
)
class FunctionViewSet(FlexFieldsMixin, ReadOnlyModelViewSet):
    """
    List organizational functions from CAMPUSonline.

    {model}
    {filter}
    {serializer}
    """

    queryset = models.Function.objects.all()
    serializer_class = serializers.FunctionSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = filters.FunctionFilter
    permission_classes = (IsAuthenticated,)
    permit_list_expands = ("persons",)


class OrganizationTypeViewSet(ReadOnlyModelViewSet):
    queryset = models.OrganizationType.objects.all()
    serializer_class = serializers.OrganizationTypeSerializer
    permission_classes = (AllowAny,)


@docstring_format(
    model=models.Organization.__doc__,
    filter=filters.OrganizationFilter.__doc__,
    serializer=serializers.OrganizationSerializer.__doc__,
)
class OrganizationViewSet(FlexFieldsMixin, ReadOnlyModelViewSet):
    """
    List organizations from CAMPUSonline.

    {model}
    {filter}
    {serializer}
    """

    queryset = models.Organization.objects.all()
    serializer_class = serializers.OrganizationSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = filters.OrganizationFilter
    permission_classes = (AllowAny,)
    permit_list_expands = (
        "persons",
        "persons_leave",
        "publication_authorship",
        "type",
        "parent",
    )

    def get_serializer_class(self):
        if self.request.user and self.request.user.is_authenticated:
            return serializers.AuthenticatedOrganizationSerializer
        else:
            return self.serializer_class

    def get_serializer_context(self):
        return {"request": self.request}


@docstring_format(
    model=models.Person.__doc__,
    filter=filters.PersonFilter.__doc__,
    serializer=serializers.PersonSerializer.__doc__,
)
class PersonViewSet(FlexFieldsMixin, ReadOnlyModelViewSet):
    """
    List staff accounts from CAMPUSonline.

    {model}
    {filter}
    {serializer}
    """

    queryset = models.Person.objects.all()
    serializer_class = serializers.PersonSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = filters.PersonFilter
    permission_classes = (AllowAny,)
    permit_list_expands = (
        "functions",
        "organizations",
        "organizations_leave",
        "classifications",
        "expertise",
        "knowledge",
        "education",
    )

    def get_serializer_class(self):
        if self.request.user and self.request.user.is_authenticated:
            return serializers.AuthenticatedPersonSerializer
        else:
            return self.serializer_class

    def get_serializer_context(self):
        return {"request": self.request}

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user and self.request.user.is_authenticated:
            return qs
        else:
            return qs.filter(employed=True)


@docstring_format(
    model=models.Student.__doc__,
    filter=filters.StudentFilter.__doc__,
    serializer=serializers.StudentSerializer.__doc__,
)
class StudentViewSet(ReadOnlyModelViewSet):
    """
    List student accounts from CAMPUSonline.

    {model}
    {filter}
    {serializer}
    """

    queryset = models.Student.objects.all()
    serializer_class = serializers.StudentSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = filters.StudentFilter
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.user and self.request.user.is_authenticated:
            return serializers.AuthenticatedStudentSerializer
        else:
            return self.serializer_class


@docstring_format(filter=filters.PersonOrganizationFunctionFilter.__doc__)
class PersonOrganizationFunctionViewSet(ReadOnlyModelViewSet):
    """
    Map person to organizational unit and function through CAMPUSonline.

    {filter}
    """

    queryset = models.PersonOrganizationFunction.objects.all()
    serializer_class = serializers.PersonOrganizationFunctionSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = filters.PersonOrganizationFunctionFilter
    permission_classes = (IsAuthenticated,)


@docstring_format(
    model=models.DistributionList.__doc__,
    filter=filters.DistributionListFilter.__doc__,
    serializer=serializers.DistributionListSerializer.__doc__,
)
class DistributionListViewSet(
    CacheResponseMixin, FlexFieldsMixin, ReadOnlyModelViewSet
):
    """
    List distribution lists from CAMPUSonline.

    {model}
    {filter}
    {serializer}
    """

    queryset = models.DistributionList.objects.all()
    serializer_class = serializers.DistributionListSerializer
    object_cache_key_func = key_constructors.DistributionListKeyConstructor()
    list_cache_key_func = key_constructors.DistributionListKeyConstructor()
    filter_backends = (DjangoFilterBackend,)
    filter_class = filters.DistributionListFilter
    permission_classes = (IsAuthenticated,)
    permit_list_expands = ("persons", "students")


@docstring_format(model=models.Event.__doc__, filter=filters.EventFilter.__doc__)
class EventViewSet(ReadOnlyModelViewSet):
    """
    List events from CAMPUSonline.

    {model}
    {filter}
    """

    queryset = models.Event.objects.all()
    serializer_class = serializers.EventSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = filters.EventFilter
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return self.queryset.filter(show_end__gte=timezone.now())


class CourseGroupTermViewSet(ReadOnlyModelViewSet):
    queryset = models.CourseGroupTerm.objects.all()
    serializer_class = serializers.CourseGroupTermSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = filters.CourseGroupTermFilter
    permission_classes = (IsAuthenticated,)


@docstring_format(model=models.Bulletin.__doc__, filter=filters.BulletinFilter.__doc__)
class BulletinViewSet(ReadOnlyModelViewSet):
    """
    List official bulletins from CAMPUSonline.

    {model}
    {filter}
    """

    queryset = models.Bulletin.objects.all()
    serializer_class = serializers.BulletinSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = filters.BulletinFilter


@docstring_format(
    model=models.BulletinPage.__doc__, filter=filters.BulletinPageFilter.__doc__
)
class BulletinPageViewSet(ReadOnlyModelViewSet):
    """
    List official bulletin pages with extracted text from CAMPUSonline.

    {model}
    {filter}
    """

    queryset = models.BulletinPage.objects.all()
    serializer_class = serializers.BulletinPageSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = filters.BulletinPageFilter
    permission_classes = (AllowAny,)


class BulletinPageSearchViewSet(HaystackViewSet):
    index_models = [models.BulletinPage]
    serializer_class = serializers.BulletinPageSearchSerializer
    permission_classes = (AllowAny,)


@docstring_format(
    model=models.FinalThesis.__doc__,
    filter=filters.FinalThesisFilter.__doc__,
    serializer=serializers.FinalThesisSerializer.__doc__,
)
class FinalThesisViewSet(FlexFieldsMixin, ReadOnlyModelViewSet):
    """
    List final thesis from CAMPUSonline.

    {model}
    {filter}
    {serializer}
    """

    queryset = models.FinalThesis.objects.all()
    serializer_class = serializers.FinalThesisSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = filters.FinalThesisFilter
    permission_classes = (IsAuthenticated,)
    permit_list_expands = ("author", "tutor", "organization")


@docstring_format(
    model=models.Country.__doc__,
    filter=filters.CountryFilter.__doc__,
    serializer=serializers.CountrySerializer.__doc__,
)
class CountryViewSet(ReadOnlyModelViewSet):
    """
    List countries from CAMPUSonline.

    {model}
    {filter}
    {serializer}
    """

    queryset = models.Country.objects.all()
    serializer_class = serializers.CountrySerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = filters.CountryFilter
    permission_classes = (AllowAny,)


@docstring_format(
    model=models.ExamMode.__doc__,
    filter=filters.ExamModeFilter.__doc__,
    serializer=serializers.ExamModeSerializer.__doc__,
)
class ExamModeViewSet(ReadOnlyModelViewSet):
    """
    List exam modes from CAMPUSonline.

    {model}
    {filter}
    {serializer}
    """

    queryset = models.ExamMode.objects.all()
    serializer_class = serializers.ExamModeSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = filters.ExamModeFilter
    permission_classes = (AllowAny,)


@docstring_format(
    model=models.ExamType.__doc__,
    filter=filters.ExamTypeFilter.__doc__,
    serializer=serializers.ExamTypeSerializer.__doc__,
)
class ExamTypeViewSet(ReadOnlyModelViewSet):
    """
    List exam types from CAMPUSonline.

    {model}
    {filter}
    {serializer}
    """

    queryset = models.ExamType.objects.all()
    serializer_class = serializers.ExamTypeSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = filters.ExamTypeFilter
    permission_classes = (AllowAny,)


@docstring_format(
    model=models.Exam.__doc__,
    filter=filters.ExamFilter.__doc__,
    serializer=serializers.ExamSerializer.__doc__,
)
class ExamViewSet(FlexFieldsMixin, ReadOnlyModelViewSet):
    """
    List exams from CAMPUSonline.

    {model}
    {filter}
    {serializer}
    """

    queryset = models.Exam.objects.all()
    serializer_class = serializers.ExamSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = filters.ExamFilter
    permission_classes = (ExtendedDjangoModelPermissions,)
    permit_list_expands = ("organization", "mode", "type", "course", "examiner")


@docstring_format(
    model=models.ExamineeStatus.__doc__,
    filter=filters.ExamineeStatusFilter.__doc__,
    serializer=serializers.ExamineeStatusSerializer.__doc__,
)
class ExamineeStatusViewSet(ReadOnlyModelViewSet):
    """
    List examinee status from CAMPUSonline.

    {model}
    {filter}
    {serializer}
    """

    queryset = models.ExamineeStatus.objects.all()
    serializer_class = serializers.ExamineeStatusSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = filters.ExamineeStatusFilter
    permission_classes = (AllowAny,)


@docstring_format(
    model=models.Examinee.__doc__,
    filter=filters.ExamineeFilter.__doc__,
    serializer=serializers.ExamineeSerializer.__doc__,
)
class ExamineeViewSet(FlexFieldsMixin, ReadOnlyModelViewSet):
    """
    List examinees from CAMPUSonline.

    {model}
    {filter}
    {serializer}
    """

    queryset = models.Examinee.objects.all()
    serializer_class = serializers.ExamineeSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = filters.ExamineeFilter
    permission_classes = (ExtendedDjangoModelPermissions,)
    permit_list_expands = ("exam", "student", "status")


@docstring_format(
    model=models.ScienceBranch.__doc__,
    filter=filters.ScienceBranchFilter.__doc__,
    serializer=serializers.ScienceBranchSerializer.__doc__,
)
class ScienceBranchViewSet(FlexFieldsMixin, ReadOnlyModelViewSet):
    """
    List science branches from CAMPUSonline.

    {model}
    {filter}
    {serializer}
    """

    queryset = models.ScienceBranch.objects.all()
    serializer_class = serializers.ScienceBranchSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = filters.ScienceBranchFilter
    permission_classes = (AllowAny,)
    permit_list_expands = ("parent",)
