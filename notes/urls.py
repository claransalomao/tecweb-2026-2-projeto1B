from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:note_id>/delete/', views.delete_note, name='delete_note'),
    path('<int:note_id>/edit/', views.edit_note, name='edit_note'),
    path('tags/', views.tags_list, name='tags_list'),
    path('tags/<int:tag_id>/', views.tag_detail, name='tag_detail'),
]