from django.db import models
from django.contrib.auth.models import User

class main(models.Model):
    Title = models.CharField(max_length=15, null=True)
    Date = models.DateField(auto_now_add=True, null=True)
    Colmn_Sep = models.CharField(max_length=2)
    Strng_Sep = models.CharField(max_length=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

class schema(models.Model):
    Name = models.CharField(max_length=50, null=True)
    Type = models.CharField(max_length=50, null=True)
    Order = models.IntegerField(null=True)
    From = models.IntegerField(null=True)
    To = models.IntegerField(null=True)
    main = models.ForeignKey(main, on_delete=models.CASCADE, null=True)

class dataset(models.Model):
    Date = models.DateField(auto_now_add=True, null=True)
    main = models.ForeignKey(main, on_delete=models.CASCADE, null=True)
    csv_file = models.FileField(upload_to='media/', null=True)


