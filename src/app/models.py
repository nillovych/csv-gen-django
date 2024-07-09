from django.contrib.auth.models import User
from django.db import models


class Main(models.Model):
    title = models.CharField(max_length=15, null=True)
    date = models.DateField(auto_now_add=True, null=True)
    column_separator = models.CharField(max_length=2)
    string_separator = models.CharField(max_length=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


class Schema(models.Model):
    name = models.CharField(max_length=50, null=True)
    data_type = models.CharField(max_length=50, null=True)
    order = models.IntegerField(null=True)
    range_from = models.IntegerField(null=True)
    range_to = models.IntegerField(null=True)
    main = models.ForeignKey(Main, on_delete=models.CASCADE, null=True)


class Dataset(models.Model):
    date = models.DateField(auto_now_add=True, null=True)
    main = models.ForeignKey(Main, on_delete=models.CASCADE, null=True)
    csv_file = models.FileField(upload_to='media/', null=True)
