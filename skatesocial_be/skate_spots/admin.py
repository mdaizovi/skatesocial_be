from django.contrib import admin

# from django_admin_listfilter_dropdown.filters import (
#     RelatedDropdownFilter,
#     ChoiceDropdownFilter,
#     DropdownFilter,
# )

from .models import City, Spot


@admin.register(Spot)
class SpotAdmin(admin.ModelAdmin):

    # list_filter = (
    #     ("category", ChoiceDropdownFilter),
    #     ("city", RelatedDropdownFilter),
    # )
    list_filter = ("category", "city")
    search_fields = ("name", "address")
    list_display = (
        "name",
        "city",
        "category",
        "city",
    )


admin.site.register(City)
