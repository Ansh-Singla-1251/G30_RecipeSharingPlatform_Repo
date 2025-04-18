from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from .models import Recipe, User, Contact
import os
import re
from django.conf import settings

def is_admin(user):
    return user.is_authenticated and (user.is_superuser or user.is_admin or user.role == 'admin')

def index(request):
    veg_filter = request.GET.get('veg', '')
    if veg_filter == '1':
        recipes = Recipe.objects.filter(is_vegetarian=True)
        selected_veg = '1'
    elif veg_filter == '0':
        recipes = Recipe.objects.filter(is_vegetarian=False)
        selected_veg = '0'
    else:
        recipes = Recipe.objects.all()
        selected_veg = ''
    return render(request, 'index.html', {'recipes': recipes, 'selected_veg': selected_veg})

def recipe_detail(request, recipe_id):
    try:
        recipe = Recipe.objects.get(pk=recipe_id)
    except Recipe.DoesNotExist:
        messages.error(request, 'Recipe not found!')
        return redirect('index')
    video_id = None
    if recipe.youtube_link:
        youtube_regex = r'(?:https?://)?(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]+)'
        match = re.search(youtube_regex, recipe.youtube_link)
        video_id = match.group(1) if match else None
    return render(request, 'recipe_detail.html', {'recipe': recipe, 'video_id': video_id})

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        feedback = request.POST['feedback']
        Contact.objects.create(name=name, email=email, feedback=feedback)
        messages.success(request, 'Thank you for your feedback! It has been submitted successfully.')
        return redirect('contact')
    return render(request, 'contact.html')

def submit(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        feedback = request.POST['feedback']
        Contact.objects.create(name=name, email=email, feedback=feedback)
        return redirect('thank_you')
    return redirect('contact')

def thank_you(request):
    return render(request, 'thank_you.html')

@login_required
def favourites(request):
    recipes = request.user.wishlist.all()
    return render(request, 'favourites.html', {'recipes': recipes})

@login_required
def wishlist(request):
    if request.user.is_authenticated:
        wishlist_items = request.user.wishlist.all()
    else:
        wishlist_items = []
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})

def breakfast(request):
    breakfast_recipes = Recipe.objects.filter(category='Breakfast')
    return render(request, 'breakfast.html', {'breakfast_recipes': breakfast_recipes})

def dinner(request):
    dinner_recipes = Recipe.objects.filter(category='Dinner')
    return render(request, 'dinner.html', {'dinner_recipes': dinner_recipes})

def lunch_recipes(request):
    lunch_recipes = Recipe.objects.filter(category='Lunch')
    return render(request, 'lunch.html', {'lunch_recipes': lunch_recipes})

def italian(request):
    italian_recipes = Recipe.objects.filter(category='Italian')
    return render(request, 'italian.html', {'italian_recipes': italian_recipes})

def mexican(request):
    mexican_recipes = Recipe.objects.filter(category='Mexican')
    return render(request, 'mexican.html', {'mexican_recipes': mexican_recipes})

def chinese(request):
    chinese_recipes = Recipe.objects.filter(category='Chinese')
    return render(request, 'chinese.html', {'chinese_recipes': chinese_recipes})

def indian(request):
    indian_recipes = Recipe.objects.filter(category='Indian')
    return render(request, 'indian.html', {'indian_recipes': indian_recipes})

def japanese(request):
    japanese_recipes = Recipe.objects.filter(category='Japanese')
    return render(request, 'japanese.html', {'japanese_recipes': japanese_recipes})

def french(request):
    french_recipes = Recipe.objects.filter(category='French')
    return render(request, 'french.html', {'french_recipes': french_recipes})

def thai(request):
    thai_recipes = Recipe.objects.filter(category='Thai')
    return render(request, 'thai.html', {'thai_recipes': thai_recipes})

def mediterranean(request):
    mediterranean_recipes = Recipe.objects.filter(category='Mediterranean')
    return render(request, 'mediterranean.html', {'mediterranean_recipes': mediterranean_recipes})

def bruschetta(request):
    return render(request, 'bruschetta.html')

def dim_sum(request):
    return render(request, 'dim_sum.html')

def nachos(request):
    return render(request, 'nachos.html')

def spring_roll(request):
    return render(request, 'spring_roll.html')

def samosa(request):
    return render(request, 'samosa.html')

def falafel(request):
    return render(request, 'falafel.html')

def poutine(request):
    return render(request, 'poutine.html')

def empandas(request):
    return render(request, 'empandas.html')

def wheel(request):
    return render(request, 'wheel.html')

def meals(request):
    return render(request, 'meals.html')

def ingredients(request):
    return render(request, 'ingredients.html')

def occasions(request):
    return render(request, 'occasions.html')

def cuisines(request):
    return render(request, 'cuisines.html')

def about(request):
    return render(request, 'about.html')

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    recipes = Recipe.objects.all()
    return render(request, 'admin_dashboard.html', {'recipes': recipes})

@login_required
@user_passes_test(is_admin)
def add_recipe(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        ingredients = request.POST['ingredients']
        instructions = request.POST['instructions']
        youtube_link = request.POST.get('youtube_link', '')
        category = request.POST['category']
        occasion = request.POST.get('occasion', '')
        price = request.POST.get('price', '0.00')
        is_vegetarian = request.POST.get('is_vegetarian') == '1'
        image = request.FILES.get('image')
        image_filename = None
        if image:
            image_filename = image.name
            image_path = os.path.join(settings.BASE_DIR, 'recipes/static/images', image.name)
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            with open(image_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
        recipe = Recipe.objects.create(
            title=title,
            description=description,
            ingredients=ingredients,
            instructions=instructions,
            youtube_link=youtube_link,
            category=category,
            occasion=occasion,
            image_filename=image_filename,
            user=request.user,
            is_vegetarian=is_vegetarian,
            price=price
        )
        messages.success(request, 'Recipe added successfully!')
        return redirect('admin_dashboard')
    return render(request, 'add_recipe.html')

@login_required
@user_passes_test(is_admin)
def edit_recipe(request, recipe_id):
    try:
        recipe = Recipe.objects.get(id=recipe_id)
    except Recipe.DoesNotExist:
        messages.error(request, 'Recipe not found!')
        return redirect('admin_dashboard')
    if request.method == 'POST':
        recipe.title = request.POST['title']
        recipe.description = request.POST['description']
        recipe.ingredients = request.POST['ingredients']
        recipe.instructions = request.POST['instructions']
        recipe.youtube_link = request.POST.get('youtube_link', '')
        recipe.category = request.POST['category']
        recipe.occasion = request.POST.get('occasion', '')
        if 'image' in request.FILES:
            image = request.FILES['image']
            image_filename = image.name
            image_path = os.path.join(settings.BASE_DIR, 'recipes/static/images', image.name)
            with open(image_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
            recipe.image_filename = image_filename
        recipe.save()
        messages.success(request, 'Recipe updated successfully!')
        return redirect('admin_dashboard')
    return render(request, 'edit_recipe.html', {'recipe': recipe})

@login_required
@user_passes_test(is_admin)
def delete_recipe(request, recipe_id):
    if request.method == 'POST':
        try:
            recipe = Recipe.objects.get(id=recipe_id)
        except Recipe.DoesNotExist:
            messages.error(request, 'Recipe not found!')
            return redirect('admin_dashboard')
        recipe.delete()
        messages.success(request, 'Recipe deleted successfully!')
        return redirect('admin_dashboard')
    return redirect('admin_dashboard')

def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        mobile = request.POST['mobile']
        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return redirect('register')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered!')
            return redirect('register')
        user = User.objects.create_user(
            name=name,
            email=email,
            mobile=mobile,
            password=password
        )
        messages.success(request, 'Registration successful! Please login.')
        return redirect('login')
    return render(request, 'register.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST.get('role', '')
        user = authenticate(request, email=email, password=password)
        if user:
            if user.role != role:
                messages.error(request, 'Please select the correct role!')
                return redirect('login')
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('index')
        messages.error(request, 'Invalid email or password!')
    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')

@login_required
def admin(request):
    if request.user.role != 'admin':
        messages.error(request, 'Access denied!')
        return redirect('index')
    return render(request, 'admin.html')

@login_required
def add_to_wishlist(request, recipe_id):
    if request.method == 'POST':
        try:
            recipe = Recipe.objects.get(id=recipe_id)
        except Recipe.DoesNotExist:
            messages.error(request, 'Recipe not found!')
            return redirect('wishlist')
        user = request.user
        if recipe in user.wishlist.all():
            user.wishlist.remove(recipe)
            messages.success(request, 'Recipe removed from wishlist!')
        else:
            user.wishlist.add(recipe)
            messages.success(request, 'Recipe added to wishlist!')
        return redirect('wishlist')
    messages.error(request, 'Invalid request!')
    return redirect('wishlist')

@login_required
def remove_from_wishlist(request, recipe_id):
    if request.method == 'POST':
        try:
            recipe = Recipe.objects.get(id=recipe_id)
        except Recipe.DoesNotExist:
            messages.error(request, 'Recipe not found!')
            return redirect('favourites')
        user = request.user
        if recipe in user.wishlist.all():
            user.wishlist.remove(recipe)
            messages.success(request, 'Recipe removed from favourites!')
        return redirect('favourites')
    return redirect('favourites')

def search(request):
    query = request.GET.get('q', '').strip()
    recipes = []
    if query:
        recipes = Recipe.objects.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) | 
            Q(category__icontains=query)
        ).distinct()
        if not recipes.exists():
            messages.info(request, f'No recipes found for "{query}".')
    else:
        messages.info(request, "Please enter a search term.")
    return render(request, 'search_results.html', {'recipes': recipes, 'query': query})