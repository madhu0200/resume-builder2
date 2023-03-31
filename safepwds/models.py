from django.db import models




class pwds(models.Model):
    id=models.IntegerField(primary_key=True)
    email=models.CharField(max_length=25)
    field=models.CharField(max_length=25)
    pwd=models.BinaryField(max_length=200)

    def __str__(self):
        return self.email