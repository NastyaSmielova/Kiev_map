from django.db import models


class District(models.Model):
    name = models.CharField(max_length=50, unique=True)
    info = models.TextField()
    shortIntro = models.CharField(max_length=200,blank=True)
    def __str__(self):
        return "%s " % (self.name)


class Street(models.Model):

   name = models.CharField(max_length=100, unique=True)
   ism_id = models.CharField(unique=True,max_length=100)
   info = models.TextField()
   districts = models.ManyToManyField(District)
   shortIntro = models.CharField(max_length=200, blank=True)

   class Meta:
        verbose_name_plural = "Streets"
   def __str__(self):
       return "%s " % (self.name)

class Question(models.Model):
    question = models.CharField(max_length=300)
    answers = models.TextField()
    correct_answer = models.CharField(max_length=10)

    def __str__(self):
        return "%s " % (self.question)


class Photos(models.Model):
    caption = models.CharField(max_length=50, unique=True)
    info = models.CharField(max_length=1500)
    districts = models.ManyToManyField(District)
    streets = models.ManyToManyField(Street, blank=True)
    file = models.CharField(max_length=100,blank=True)

    def __str__(self):
        return "%s " % (self.caption)

# Create your models here.
