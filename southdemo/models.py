from django.db import models

# Create your models here.
class Lizard(models.Model):
    
    age = models.IntegerField()
    name = models.CharField(max_length=30)
    fucker = models.CharField(max_length=30, default='Bobby')


class Adopter(models.Model):
    
    lizard = models.ForeignKey(Lizard)
    name = models.CharField(max_length=50)

primary_key_bing = 'yr8m3Mf+wzjJS+JsRyFqE6ENbWhHLCM14DDbQsNCnak'