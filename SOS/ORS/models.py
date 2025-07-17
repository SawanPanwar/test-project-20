from django.db import models


class User(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    loginId = models.EmailField()
    password = models.CharField(max_length=20)
    confirmPassword = models.CharField(max_length=20, default='')
    dob = models.DateField(max_length=20)
    address = models.CharField(max_length=50, default='')
    gender = models.CharField(max_length=50, default='')
    mobileNumber = models.CharField(max_length=50, default='')
    roleId = models.IntegerField()
    roleName = models.CharField(max_length=50)

    class Meta:
        db_table = 'sos_user'


class Role(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)

    class Meta:
        db_table = 'sos_role'


class College(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=20)
    phoneNumber = models.CharField(max_length=20)

    class Meta:
        db_table = 'sos_college'


class Course(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)

    class Meta:
        db_table = 'sos_course'



