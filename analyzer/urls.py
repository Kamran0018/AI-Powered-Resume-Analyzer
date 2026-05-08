from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_resume, name='upload_resume'),
    path('result/<int:resume_id>/', views.result_view, name='result'),
    path('match/<int:resume_id>/', views.match_job, name='match_job'),
    path('history/', views.resume_history, name='resume_history'),
]