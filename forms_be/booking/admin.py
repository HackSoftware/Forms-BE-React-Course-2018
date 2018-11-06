# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Meal, BookingRequest, RoomType


@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(BookingRequest)
class BookingRequestAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'email',
        'phone',
        'start',
        'end',
        'room_type',
        'meal',
        'number_of_people',
        'notes'
    )
