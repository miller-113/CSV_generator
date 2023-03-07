from django.contrib.auth import views as auth_views
from django.urls import path
from .views import view_schema, create_schema, schema_detail,\
    generate_data, download_csv


urlpatterns = [
    path('', view_schema, name='schema'),
    path('create/', create_schema, name='create_schema'),
    path('<int:schema_id>', schema_detail, name='schema_detail'),
    path('generate-data/<int:schema_id>', generate_data, name='generate_data'),
    path('download_csv/<int:dataset_id>', download_csv, name='download_csv'),
]
