from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('favorites/', views.favorites, name='favorites'),
    path('add_favorite/', views.add_favorite, name='add_favorite'),
    path('remove_favorite/<str:event_id>/', views.remove_favorite, name='remove_favorite'),
    path('update_favorite/<str:event_id>/', views.update_favorite, name='update_favorite'),
]
