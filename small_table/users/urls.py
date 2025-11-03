from django.urls import path
from . import views

urlpatterns = [
     path('createUser/', views.create_user, name='create_user'),
     path('deleteUser/', views.delete_user, name='delete_user'),
     path('editUser/', views.edit_user, name='edit_user'),
     path('getAllUsers/', views.get_all_users, name='get_all_users'),
     path('getUserById/<string:id>/', views.get_user_by_id, name='get_user_by_id'),
]
