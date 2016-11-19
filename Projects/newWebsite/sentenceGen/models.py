from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Sentence(models.Model):
    text = models.CharField(max_length=1000)

class Quiz(models.Model):
    name = models.CharField(max_length = 20)
    score = models.IntegerField(default = 0)
    attempts = models.IntegerField(default = 0)
    mode = models.CharField(max_length = 20)
    teacher = models.CharField(max_length = 20)
    old_questions = models.CharField(max_length = 200)

class Question(models.Model):
    sentence = models.CharField(max_length = 200)
    wordPKs = models.CharField(max_length = 200)
    chosen_words = models.CharField(max_length = 200)
    correct_words = models.CharField(max_length = 200)

class Word(models.Model):
    question = models.ForeignKey(Question, on_delete = models.CASCADE)
    word = models.CharField(max_length = 20)
    part_of_speech = models.CharField(max_length = 20)
    index = models.IntegerField(default = 0)

class Teacher(models.Model):
    code = models.CharField(max_length = 20)
    password = models.CharField(max_length = 20)

# class Student(models.Model):
#     name = models.CharField(max_length = 20)
#     password = models.CharField(max_length = 8)

# from django.db import models

# CATEGORIES = (  
#     ('LAB', 'labor'),
#     ('CAR', 'cars'),
#     ('TRU', 'trucks'),
#     ('WRI', 'writing'),
# )
# LOCATIONS = (  
#     ('BRO', 'Bronx'),
#     ('BRK', 'Brooklyn'),
#     ('QNS', 'Queens'),
#     ('MAN', 'Manhattan'),
#     ('STN', 'Staten Island'),
# )

# class PostAd(models.Model):  
#     name        = models.CharField(max_length=50)
#     email       = models.EmailField()
#     gist        = models.CharField(max_length=50)
#     category    = models.CharField(max_length=3, choices=CATEGORIES)
#     location    = models.CharField(max_length=3, choices=LOCATIONS)
#     description = models.TextField(max_length=300)
#     expire      = models.DateField()