# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone


class RoomType(models.Model):
    name = models.CharField(max_length=255)


class Meal(models.Model):
    name = models.CharField(max_length=255)


class Room(models.Model):
    number = models.CharField(max_length=255)
    available = models.BooleanField(default=True)
    room_type = models.ForeignKey(RoomType, null=True, blank=True)


class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=255, null=True)


class BookingRequest(models.Model):
    start = models.DateField()
    end = models.DateField()
    created_at = models.DateTimeField(default=timezone.now)

    user = models.ForeignKey(User, null=True, blank=True)
    room_type = models.ForeignKey(RoomType)
    room = models.ForeignKey(Room, null=True, blank=True)
    meal = models.ForeignKey(Meal, null=True, blank=True)
    number_of_people = models.IntegerField(null=True, blank=True)

    notes = models.CharField(max_length=255, null=True)
