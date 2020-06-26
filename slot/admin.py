from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(User, RoomSlot, Event, Request )
class ViewAdmin(admin.ModelAdmin):
    pass
