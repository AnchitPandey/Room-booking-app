# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class faculty(models.Model):
    faculty_name = models.CharField(max_length=40)
    password = models.CharField(max_length=50)
    upsn = models.CharField(max_length=13,primary_key=True)
    def __str__(self):
        return self.faculty_name

class reservation(models.Model):
    room_no = models.CharField(max_length=13)
    faculty_name = models.CharField(max_length = 40)
    date = models.CharField(max_length = 40, default = None)
    start_time = models.CharField(max_length=13)
    end_time = models.CharField(max_length=13)
    event_name = models.CharField(max_length = 40, default='')
    def __str__(self):
        return self.room_no


class Admin(models.Model):
    username = models.CharField(max_length = 30)
    password = models.CharField(max_length = 20)
    def __str__(self):
        return self.username
        
