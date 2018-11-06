# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class RoomType(models.Model):
    name = models.CharField(max_length=255)


class Meal(models.Model):
    name = models.CharField(max_length=255)


class BookingRequest(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=255)

    start = models.DateField()
    end = models.DateField()

    room_type = models.ForeignKey(RoomType)
    meal = models.ForeignKey(Meal)
    number_of_people = models.IntegerField()

    notes = models.CharField(max_length=255)
