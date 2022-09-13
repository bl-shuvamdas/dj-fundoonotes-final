from django.urls import path

from . import views

app_name = 'noteq'

urlpatterns = [
    path('', views.NoteRawQAPIView.as_view(), name='note'),
    path('<int:pk>/', views.NoteRawQAPIView.as_view(), name='note_detail'),
]
