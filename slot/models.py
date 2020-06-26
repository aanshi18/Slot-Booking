from datetime import date

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime
from django.core.exceptions import ValidationError
#import django.utils.timezone.now

# Create your models here.


class User(models.Model):
    userName = models.CharField(max_length=100, blank='false',primary_key='true')
    userId = models.IntegerField()
    type = (
        ('Admin', 'admin'),
        ('Faculty', 'faculty'),
        ('Club', 'club')
    )
    userType = models.CharField(max_length=10, choices=type, default="Faculty")
    userMailId = models.CharField(max_length=100, default="@ahduni.edu.in")
    userPassword = models.CharField(max_length=100, blank='false')

    def __str__(self):
        return 'Type : {0} Name : {1}'.format(self.userType, self.userName)



class RoomSlot(models.Model):
    rsId = models.AutoField(primary_key='true')
    rsUserName = models.ForeignKey(User, default='faculty', on_delete=models.SET_DEFAULT)
    type1 = (
        ('9.30-11', '9.30 - 11'),
        ('11-12.30', '11 - 12.30'),
        ('1-2.30', '1 - 2.30'),
        ('2.30-4', '2.30 - 4'),
        ('4-5.30', '4 - 5.30'),
        ('5.30-7', '5.30 - 7'),
    )
    slotId = models.CharField(max_length=10, choices=type1, default="1")
    type2 = (
        ('001', '001'),
        ('005', '005'),
        ('105', '105'),
        ('116', '116')
    )
    roomNum = models.CharField(max_length=10, choices=type2, default="005")
    type3 = (
        ('Classroom', 'classroom'),
        ('Lab', 'lab'),
        ('Auditorium', 'auditorium')
    )
    roomType = models.CharField(max_length=10, choices=type3, default="Classroom")
    roomCapacity = models.IntegerField(validators=[MinValueValidator(25), MaxValueValidator(300)])
    slotDate = models.DateField(auto_now='false')

    class Meta:
        unique_together = (("slotId", "roomNum", "slotDate"),)


class Event(models.Model):
    eventId = models.CharField(max_length=8,default='LECXXX',primary_key='true')
    #rs_event = models.ForeignKey(RoomSlot, default=1, on_delete=models.SET_DEFAULT)
    eUser = models.ForeignKey(User, default=1, on_delete=models.SET_DEFAULT)
    eventName = models.CharField(max_length=50, blank='false')
    eventDesc = models.TextField(max_length=250,default='Event or Lecture')

    def __str__(self):
        return ' Event : {0}'.format(self.eventId)


class Request(models.Model):
    #reqId = models.AutoField(primary_key='true')
    rEvent = models.ForeignKey(Event, default='LEC', on_delete=models.SET_DEFAULT)
    rUser = models.ForeignKey(User, default='faculty', on_delete=models.SET_DEFAULT)
    rSlot = models.CharField(max_length=15,  default="1")
    rDate = models.CharField(max_length=20,  default=" ")
    rRoom = models.CharField(max_length=10, default="005")
    type = (
        ('Accepted', 'accept'),
        ('Declined', 'decline'),

    )
    reqStatus = models.CharField(max_length=10, choices=type, default="Declined")
    fbDesc = models.TextField()


""" def save(self, *args, **kwargs):
        if self.slotDate < datetime.date.today():
            raise ValidationError("The date cannot be in the past!")
        super(RoomSlot, self).save(*args, **kwargs)"""
