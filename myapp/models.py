from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Expert(models.Model):
    name=models.CharField(max_length=100)
    email_id=models.CharField(max_length=150)
    dob=models.CharField(max_length=130)
    phone_no=models.CharField(max_length=140)
    place=models.CharField(max_length=120)
    post=models.CharField(max_length=120)
    pin_code=models.CharField(max_length=120)
    qualification=models.CharField(max_length=123)
    experience=models.CharField(max_length=151)
    photo=models.CharField(max_length=253)
    USER = models.OneToOneField(User, on_delete=models.CASCADE)

class Video(models.Model):
     title=models.CharField(max_length=225)
     video=models.CharField(max_length=333)
     EXPERT=models.ForeignKey(Expert,on_delete=models.CASCADE)


class  Usertable(models.Model):
    name=models.CharField(max_length=100)
    email_id=models.CharField(max_length=150)
    phone_no=models.CharField(max_length=140)
    place=models.CharField(max_length=120)
    pin_code=models.CharField(max_length=120)
    post=models.CharField(max_length=120)
    photo=models.CharField(max_length=253)
    USER=models.OneToOneField(User,on_delete=models.CASCADE)




class complaint(models.Model):
    date=models.DateField()
    complaint=models.CharField(max_length=232)
    reply=models.CharField(max_length=232)
    status=models.CharField(max_length=232)
    USER=models.ForeignKey(Usertable,on_delete=models.CASCADE)


class  chattable(models.Model):
       FROMC = models.ForeignKey(User, on_delete=models.CASCADE,related_name="fromc")
       TOC= models.ForeignKey(User, on_delete=models.CASCADE,related_name="toc")
       date = models.DateField()
       message=models.CharField(max_length=500)
       is_read = models.BooleanField(default=False)


class  Review(models.Model):
    date=models.DateField()
    review=models.CharField(max_length=500)
    CUSTOMER=models.ForeignKey(Usertable, on_delete=models.CASCADE)
    rating=models.CharField(max_length=100)


class logs(models.Model):
    date=models.DateField()
    time= models.TimeField()
    ipaddress=models.CharField(max_length=100)
    log=models.CharField(max_length=100)
    CUSTOMER = models.ForeignKey(Usertable, on_delete=models.CASCADE)


class logss(models.Model):
    date=models.DateField()
    time= models.TimeField()
    ipaddress=models.CharField(max_length=100)
    log=models.CharField(max_length=100)
    CUSTOMER = models.ForeignKey(Usertable, on_delete=models.CASCADE)



