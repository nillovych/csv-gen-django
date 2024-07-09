from django.contrib import admin

from .models import Main, Schema, Dataset

admin.site.register(Main)
admin.site.register(Schema)
admin.site.register(Dataset)
