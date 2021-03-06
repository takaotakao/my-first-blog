from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post_list_Serch/<int:id>/', views.post_list_Serch, name='post_list_Serch'),
    #path('exercise', views.exercise, name='exercise'),
    path('redisp', views.post_list, name='redisp'),
    path('post_memberset', views.post_memberset, name='post_memberset')
]

