from django.urls import path

from . import views

app_name = 'seed'

urlpatterns = [
    path('users/', views.users, name='users'),
    path('items/', views.items, name='items'),
    path('categories/', views.categories, name='categories'),
]
