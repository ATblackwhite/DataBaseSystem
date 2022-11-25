from django.db import models
import uuid

class Member(models.Model):
    memberNumber = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=10)
    age = models.IntegerField(blank=True)
    sex = models.CharField(max_length=5, choices=[('1', 'boy'), ('2', 'girl')])
    passwd = models.CharField(max_length=20, default=None)
    session = models.UUIDField(max_length=32, default=uuid.uuid4, editable=True, null=True)
    level = models.CharField(max_length=10, choices=[('1', 'normal'), ('2', 'principal'), ('3', 'admin')])

class Club(models.Model):
    clubNumber = models.CharField(max_length=8, primary_key=True)
    name = models.CharField(max_length=20)
    principal = models.ForeignKey(Member, on_delete=models.RESTRICT)


class Join(models.Model):
    member = models.ForeignKey(Member, on_delete=models.RESTRICT)
    club = models.ForeignKey(Club, on_delete=models.RESTRICT)
    attendDate = models.DateTimeField()
    confirm = models.BooleanField(null=True, default=False)


class Activity(models.Model):
    number = models.CharField(max_length=8, primary_key=True)
    name = models.CharField(max_length=20)
    club = models.ForeignKey(Club, on_delete=models.RESTRICT)
    principal = models.ForeignKey(Member, on_delete=models.RESTRICT)
    location = models.CharField(max_length=20)
    dateTime = models.DateTimeField(default=None)
    maxNumber = models.IntegerField(default=0)
    memberNumber = models.IntegerField(default=0)


class Attend(models.Model):
    member = models.ForeignKey(Member, on_delete=models.RESTRICT)
    activity = models.ForeignKey(Activity, on_delete=models.RESTRICT)

# Create your models here.

