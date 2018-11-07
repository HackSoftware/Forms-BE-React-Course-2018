# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone


class RoomType(models.Model):
    name = models.CharField(max_length=255)


class Meal(models.Model):
    name = models.CharField(max_length=255)


class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255, null=True)


class BookingRequest(models.Model):
    start = models.DateField()
    end = models.DateField()
    created_at = models.DateTimeField(default=timezone.now)

    user = models.ForeignKey(User, null=True, blank=True)
    room_type = models.ForeignKey(RoomType)
    meal = models.ForeignKey(Meal)
    number_of_people = models.IntegerField(null=True, blank=True)

    notes = models.CharField(max_length=255, null=True)
