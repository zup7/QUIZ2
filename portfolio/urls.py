from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    path('', views.applicant_list, name='list'),
    path('portfolio/<str:username>/', views.ApplicantDetailView.as_view(), name='detail'),
    path('delete/<str:username>/', views.ApplicantDeleteView.as_view(), name='delete'),
]
