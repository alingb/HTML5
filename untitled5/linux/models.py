from django.db import models

# Create your models here.

class Teacher(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    sex = models.CharField(max_length=10)
    subject = models.CharField(max_length=50)
    telphone = models.CharField(max_length=30)

    class Meta:
        db_table = "linux_teacher"