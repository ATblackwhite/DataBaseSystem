from django.db import models
import uuid

class Member(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=10)
    age = models.IntegerField(blank=True)
    sex = models.CharField(max_length=5, choices=[('1', 'boy'), ('2', 'girl')])
    passwd = models.CharField(max_length=20, default=None)
    level = models.CharField(max_length=10, choices=[('1', 'normal'), ('2', 'principal'), ('3', 'admin')])


class Club(models.Model):
    id = models.CharField(max_length=8, primary_key=True)
    name = models.CharField(max_length=20)
    principal = models.ForeignKey(Member, on_delete=models.CASCADE)


class Join(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    attendDate = models.DateTimeField()
    confirm = models.BooleanField(null=True, default=False)


class Activity(models.Model):
    name = models.CharField(max_length=20)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    location = models.CharField(max_length=20)
    dateTime = models.DateTimeField(default=None)
    maxNumber = models.IntegerField(default=0)
    memberNumber = models.IntegerField(default=0)


class Attend(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)

# Create your models here.

