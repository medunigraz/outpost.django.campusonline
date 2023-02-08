from . import api

v1 = [
    (r"campusonline/room", api.RoomViewSet, "campusonline-room"),
    (r"campusonline/function", api.FunctionViewSet, "campusonline-function"),
    (
        r"campusonline/organization",
        api.OrganizationViewSet,
        "campusonline-organization",
    ),
    (r"campusonline/person", api.PersonViewSet, "campusonline-person"),
    (r"campusonline/student", api.StudentViewSet, "campusonline-student"),
    (
        r"campusonline/personorganizationfunction",
        api.PersonOrganizationFunctionViewSet,
        "campusonline-personorganizationfunction",
    ),
    (
        r"campusonline/distributionlist",
        api.DistributionListViewSet,
        "campusonline-distributionlist",
    ),
    (r"campusonline/finalthesis", api.FinalThesisViewSet, "campusonline-finalthesis"),
    (r"campusonline/event", api.EventViewSet, "campusonline-event"),
    (
        r"campusonline/bulletin:page",
        api.BulletinPageViewSet,
        "campusonline-bulletin-page",
    ),
    (r"campusonline/bulletin", api.BulletinViewSet, "campusonline-bulletin"),
    (
        r"campusonline/search/bulletin:page",
        api.BulletinPageSearchViewSet,
        "campusonline-search-bulletin-page",
    ),
    (
        r"campusonline/course-group-term",
        api.CourseGroupTermViewSet,
        "campusonline-course-group-term",
    ),
    (
        r"campusonline/country",
        api.CountryViewSet,
        "campusonline-country",
    ),
    (
        r"campusonline/exam:mode",
        api.ExamModeViewSet,
        "campusonline-exam-mode",
    ),
    (
        r"campusonline/exam:type",
        api.ExamTypeViewSet,
        "campusonline-exam-type",
    ),
    (
        r"campusonline/exam",
        api.ExamViewSet,
        "campusonline-exam",
    ),
    (
        r"campusonline/examinee:status",
        api.ExamineeStatusViewSet,
        "campusonline-examinee-status",
    ),
    (
        r"campusonline/examinee",
        api.ExamineeViewSet,
        "campusonline-examinee",
    ),
]
