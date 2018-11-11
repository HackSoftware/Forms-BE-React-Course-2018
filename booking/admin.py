# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Meal, BookingRequest, RoomType, User, Room


@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(BookingRequest)
class BookingRequestAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'start',
        'end',
        'room_type',
        'meal',
        'number_of_people',
        'notes'
    )


@admin.register(User)
class User(admin.ModelAdmin):
    list_display = (
        'name',
        'email',
        'phone',
)


@admin.register(Room)
class Room(admin.ModelAdmin):
    list_display = (
        'number',
        'available',
        'room_type'
)