# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        all_users = User.objects.all()
        if len(postData['name']) < 2:
            errors['name'] = "name should be more than 2 characters"
        if len(postData['alias']) < 2:
            errors['alias'] = "Alias should be more than 2 characters"
        if postData['alias'].isalpha() == False:
            errors['alias'] = "alias cannot contain any numbers"
        if len(postData['email']) < 1:
            errors['email'] = "Email field cannot be blank"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address"
        if len(postData['password']) < 8:
            errors['password'] = "Password cannot be less then 8 characters"
        if not postData['password'] == postData['confirm_pw']:
            errors['password'] = "Password fields dont match"
        for user in all_users:
            if postData['email'] == user.email:
                errors['email'] = "Email already used"
        return errors

    def login_validator(self, postData):
        errors = {}
        if len(postData['email']) < 1:
            errors['email'] = "Email field cannot be blank"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address"
        if len(postData['password']) < 8:
            errors['password'] = "Password cannot be less then 8 characters"
        return errors

    def qoute_validator(self, postData):
        errors = {}
        if len(postData['qouted_by']) < 3:
            errors['qouted_by'] = "must be more than 3 characters."
        if len(postData['message']) < 10:
            errors['message'] = "must be more than 10 characters."
        return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=72)
    dob = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

    def __str__(self):
        return "First Name: {}, Last Name: {}, Email: {}, Password: {}\n".format(self.first_name, self.last_name, self.email, self.password)

class Qoute(models.Model):
    qouted_by = models.CharField(max_length=255)
    message = models.CharField(max_length=500)
    user = models.ForeignKey(User, related_name="qoutes")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

    def __str__(self):
        return "Qouted_by : {}, Message : {}\n".format(self.qouted_by, self.message)

class Favorite(models.Model):
    qoute_author = models.CharField(max_length=255)
    qoute_message = models.CharField(max_length=500)
    user = models.ForeignKey(User, related_name="favorites")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return "Qoute_author : {}, Qoute_message : {}\n".format(self.qoute_author, self.qoute_message)