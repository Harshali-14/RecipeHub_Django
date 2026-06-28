from rest_framework import serializers
from .models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    total_time = serializers.ReadOnlyField()
    avg_rating = serializers.ReadOnlyField()
    rating_count = serializers.ReadOnlyField()

    class Meta:
        model = Recipe
        fields = [
            'id',
            'author',
            'title',
            'description',
            'category',
            'difficulty',
            'prep_time',
            'cook_time',
            'total_time',
            'servings',
            'ingredients',
            'instructions',
            'image',
            'avg_rating',
            'rating_count',
            'is_featured',
            'created_at',
            'updated_at',
        ]