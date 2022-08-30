from django.urls import path

from . import views

app_name = 'note'

urlpatterns = [
    path('', views.NoteAPIView.as_view(), name='note_detail'),
    path('collab/', views.CollaboratorAPIView.as_view(), name='collaborator'),
]
