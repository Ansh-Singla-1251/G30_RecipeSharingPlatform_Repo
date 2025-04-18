from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recipe/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('contact/', views.contact, name='contact'),
    path('submit/', views.submit, name='submit'),
    path('thank-you/', views.thank_you, name='thank_you'),
    path('favourites/', views.favourites, name='favourites'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('breakfast/', views.breakfast, name='breakfast'),
    path('dinner/', views.dinner, name='dinner'),
    path('lunch/', views.lunch_recipes, name='lunch'),
    path('italian/', views.italian, name='italian'),
    path('mexican/', views.mexican, name='mexican'),
    path('chinese/', views.chinese, name='chinese'),
    path('indian/', views.indian, name='indian'),
    path('japanese/', views.japanese, name='japanese'),
    path('french/', views.french, name='french'),
    path('thai/', views.thai, name='thai'),
    path('mediterranean/', views.mediterranean, name='mediterranean'),
    path('wheel/', views.wheel, name='wheel'),
    path('nachos/', views.nachos, name='nachos'),
    path('spring_roll/', views.spring_roll, name='spring_roll'),
    path('Samosa/', views.samosa, name='samosa'),
    path('bruschetta/', views.bruschetta, name='bruschetta'),
    path('falafel/', views.falafel, name='falafel'),
    path('Poutine/', views.poutine, name='poutine'),
    path('empandas/', views.empandas, name='empandas'),
    path('dim_sum/', views.dim_sum, name='dim_sum'),
    path('meals/', views.meals, name='meals'),
    path('ingredients/', views.ingredients, name='ingredients'),
    path('occasions/', views.occasions, name='occasions'),
    path('cuisines/', views.cuisines, name='cuisines'),
    path('about/', views.about, name='about'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('recipe/add/', views.add_recipe, name='add_recipe'),
    path('recipe/<int:recipe_id>/edit/', views.edit_recipe, name='edit_recipe'),
    path('recipe/<int:recipe_id>/delete/', views.delete_recipe, name='delete_recipe'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin/', views.admin, name='admin'),
    path('add_to_wishlist/<int:recipe_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove_favorite/<int:recipe_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('search/', views.search, name='search'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add_recipe/', views.add_recipe, name='add_recipe'),
    path('edit_recipe/<int:recipe_id>/', views.edit_recipe, name='edit_recipe'),
    path('delete_recipe/<int:recipe_id>/', views.delete_recipe, name='delete_recipe'),
]