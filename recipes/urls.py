from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('recipes/', views.recipe_list, name='recipe_list'),
    path('recipes/create/', views.recipe_create, name='recipe_create'),
    path('recipes/<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('recipes/<int:pk>/edit/', views.recipe_edit, name='recipe_edit'),
    path('recipes/<int:pk>/delete/', views.recipe_delete, name='recipe_delete'),
    path('recipes/<int:pk>/rate/', views.rate_recipe, name='rate_recipe'),
    path('recipes/<int:pk>/save/', views.toggle_save, name='toggle_save'),
    path('my-recipes/', views.my_recipes, name='my_recipes'),
    path('comments/<int:pk>/delete/', views.delete_comment, name='delete_comment'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
