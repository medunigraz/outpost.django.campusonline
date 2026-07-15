from django.contrib import admin

from outpost.django.base.admin import ReadOnlyAdminMixin

from . import models


@admin.register(models.Organization)
class OrganizationAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = ("__str__", "short", "parent", "type", "address")
    list_display_links = ("__str__", "short")
    list_filter = ("category", "type", "university_law")
    search_fields = ("name", "short")


@admin.register(models.Person)
class PersonAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = ("last_name", "first_name", "title", "email", "username", "room")
    list_display_links = ("first_name", "last_name")
    list_filter = ("sex", "employed")
    search_fields = ("first_name", "last_name", "email")
    exclude = ("avatar_private", "hash")


@admin.register(models.Student)
class StudentAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = ("last_name", "first_name", "email", "username", "cardid")
    list_display_links = ("first_name", "last_name")


class PersonInline(admin.TabularInline):
    model = models.Person.distribution_list_internal.through


@admin.register(models.DistributionListInternal)
class DistributionListInternalAdmin(admin.ModelAdmin):
    inlines = [PersonInline]


@admin.register(models.BulletinPage)
class BulletinPageAdmin(admin.ModelAdmin):
    list_display = ("bulletin", "index", "clean")
    list_display_links = ("index",)
    list_filter = ("clean",)
    readonly_fields = ("bulletin", "index")
