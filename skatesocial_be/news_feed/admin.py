from django.contrib import admin

from .models import Event, EventResponse

admin.site.register(Event)
admin.site.register(EventResponse)
