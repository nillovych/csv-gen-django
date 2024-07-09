from django.urls import path

from .views import new_schema, getting, main_view, delete_row, edit, getting_edit, datasets, generate, download_csv

urlpatterns = [
    path('add_new/', new_schema, name='new_schema'),
    path('', main_view, name='home'),
    path('download_csv/<int:dataset_id>/', download_csv, name='download_csv'),
    path('edit/<int:data_id>/', edit, name='edit'),
    path('datasets/<int:data_id>/', datasets, name='datasets'),
    path('getting/', getting, name='getting'),
    path('generate/', generate, name='generate'),
    path('getting_edit/', getting_edit, name='getting_edit'),
    path('delete_row/', delete_row, name='delete-row'),
]
