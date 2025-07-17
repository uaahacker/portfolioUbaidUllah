from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('projects/', views.ProjectsView.as_view(), name='projects'),
    path('project/<int:pk>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('resources/', views.ResourcesView.as_view(), name='resources'),
    path('resources/download/<int:pk>/', views.ResourceDownloadView.as_view(), name='resource_download'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('contact/ajax/', views.ContactAjaxView.as_view(), name='contact_ajax'),
]
