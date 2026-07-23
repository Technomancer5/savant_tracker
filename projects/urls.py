from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path("project/new/", views.create_project, name="create_project"),
    path('upload-csv/', views.upload_csv, name='upload_csv'),
    path('export-csv/', views.export_csv, name='export_csv'),
    path('project/<int:pk>/', views.project_detail, name='project_detail'),
    path('project/<int:pk>/edit/', views.edit_project, name='edit_project'),
     path('project/<int:pk>/delete/', views.delete_project, name='delete_project'),
]
