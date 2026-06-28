from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Avg
from .models import Recipe, Rating, SavedRecipe, Comment
from .forms import RecipeForm, CommentForm, RatingForm, RegisterForm
from django.contrib.auth.decorators import login_required

CATEGORY_EMOJIS = {
    'breakfast': '🍳',
    'lunch': '🥗',
    'dinner': '🍽️',
    'dessert': '🍰',
    'snack': '🍿',
    'drinks': '🥤',
}

def home(request):
    featured = Recipe.objects.filter(is_featured=True)[:3]
    recent = Recipe.objects.order_by('-created_at')[:8]
    top_rated = Recipe.objects.all()
    # Sort by avg rating in Python since SQLite aggregation is simple
    top_rated = sorted(top_rated, key=lambda r: r.avg_rating or 0, reverse=True)[:4]
    total_recipes = Recipe.objects.count()
    context = {
        'featured': featured,
        'recent': recent,
        'top_rated': top_rated,
        'total_recipes': total_recipes,
        'category_emojis': CATEGORY_EMOJIS,
    }
    return render(request, 'recipes/home.html', context)


def recipe_list(request):
    recipes = Recipe.objects.all().order_by('-created_at')
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    difficulty = request.GET.get('difficulty', '')
    sort = request.GET.get('sort', 'newest')

    if query:
        recipes = recipes.filter(Q(title__icontains=query) | Q(description__icontains=query) | Q(ingredients__icontains=query))
    if category:
        recipes = recipes.filter(category=category)
    if difficulty:
        recipes = recipes.filter(difficulty=difficulty)

    recipes = list(recipes)
    if sort == 'top_rated':
        recipes = sorted(recipes, key=lambda r: r.avg_rating or 0, reverse=True)
    elif sort == 'quickest':
        recipes = sorted(recipes, key=lambda r: r.total_time)

    context = {
        'recipes': recipes,
        'query': query,
        'category': category,
        'difficulty': difficulty,
        'sort': sort,
        'category_emojis': CATEGORY_EMOJIS,
    }
    return render(request, 'recipes/recipe_list.html', context)

@login_required(login_url='login')
def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    comments = recipe.comments.select_related('user').order_by('-created_at')
    user_rating = None
    user_saved = False

    if request.user.is_authenticated:
        user_rating = Rating.objects.filter(recipe=recipe, user=request.user).first()
        user_saved = SavedRecipe.objects.filter(recipe=recipe, user=request.user).exists()

    comment_form = CommentForm()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'Please login to comment.')
            return redirect('login')
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            c = comment_form.save(commit=False)
            c.recipe = recipe
            c.user = request.user
            c.save()
            messages.success(request, 'Comment added!')
            return redirect('recipe_detail', pk=pk)

    related = Recipe.objects.filter(category=recipe.category).exclude(pk=pk)[:3]
    context = {
        'recipe': recipe,
        'comments': comments,
        'comment_form': comment_form,
        'user_rating': user_rating,
        'user_saved': user_saved,
        'related': related,
        'ingredients': recipe.get_ingredients_list(),
        'instructions': recipe.get_instructions_list(),
    }
    return render(request, 'recipes/recipe_detail.html', context)

@login_required
def recipe_create(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            messages.success(request, f'"{recipe.title}" created!')
            return redirect('recipe_detail', pk=recipe.pk)
    else:
        form = RecipeForm()
    return render(request, 'recipes/recipe_form.html', {'form': form, 'action': 'Create'})

@login_required
def recipe_edit(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, author=request.user)
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            messages.success(request, 'Recipe updated!')
            return redirect('recipe_detail', pk=pk)
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'recipes/recipe_form.html', {'form': form, 'action': 'Edit', 'recipe': recipe})

@login_required
def recipe_delete(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, author=request.user)
    if request.method == 'POST':
        title = recipe.title
        recipe.delete()
        messages.success(request, f'"{title}" deleted.')
        return redirect('recipe_list')
    return render(request, 'recipes/recipe_confirm_delete.html', {'recipe': recipe})

@login_required
def rate_recipe(request, pk):
    if request.method == 'POST':
        recipe = get_object_or_404(Recipe, pk=pk)
        score = int(request.POST.get('score', 0))
        if 1 <= score <= 5:
            Rating.objects.update_or_create(recipe=recipe, user=request.user, defaults={'score': score})
        return JsonResponse({'avg': recipe.avg_rating, 'count': recipe.rating_count})
    return JsonResponse({'error': 'Invalid'}, status=400)

@login_required
def toggle_save(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    saved, created = SavedRecipe.objects.get_or_create(recipe=recipe, user=request.user)
    if not created:
        saved.delete()
        return JsonResponse({'saved': False})
    return JsonResponse({'saved': True})

@login_required
def my_recipes(request):
    recipes = Recipe.objects.filter(author=request.user).order_by('-created_at')
    saved = SavedRecipe.objects.filter(user=request.user).select_related('recipe').order_by('-saved_at')
    return render(request, 'recipes/my_recipes.html', {'recipes': recipes, 'saved': saved})

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk, user=request.user)
    recipe_pk = comment.recipe.pk
    comment.delete()
    messages.success(request, 'Comment deleted.')
    return redirect('recipe_detail', pk=recipe_pk)

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.username}!')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'recipes/auth.html', {'form': form, 'action': 'Register'})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(request.GET.get('next', 'home'))
        messages.error(request, 'Invalid credentials.')
    else:
        form = AuthenticationForm()
    return render(request, 'recipes/auth.html', {'form': form, 'action': 'Login'})
@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('home')
