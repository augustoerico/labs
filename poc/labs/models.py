from django.db import models

class Responsible(models.Model):
	username = models.CharField(max_length=30)

class Laboratory(models.Model):
	responsibles = models.ManyToManyField(Responsible)
	
	tag = models.CharField(max_length=30)

class Project(models.Model):
	laboratory = models.ForeignKey(Laboratory)
	responsible = models.ForeignKey(Responsible)
	
	tag = models.CharField(max_length=30)
	start_date = models.DateField()
	
class Budget(models.Model):
	project = models.ForeignKey(Project)
	
	in_date = models.DateField()
	value = models.DecimalField(max_digits=12, decimal_places=2)
