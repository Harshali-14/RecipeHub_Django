from django.contrib import admin
from .models import Recipe, Rating, SavedRecipe, Comment


class RatingInline(admin.TabularInline):
    model = Rating
    extra = 0
    readonly_fields = ("user", "score", "created_at")


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ("user", "created_at")


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "category",
        "difficulty",
        "servings",
        "total_time",
        "is_featured",
        "created_at",
    )

    list_filter = (
        "category",
        "difficulty",
        "is_featured",
        "created_at",
    )

    search_fields = (
        "title",
        "description",
        "author__username",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "total_time",
    )

    list_editable = (
        "is_featured",
    )

    ordering = (
        "-created_at",
    )

    inlines = [
        RatingInline,
        CommentInline,
    ]

    fieldsets = (
        ("Basic Information", {
            "fields": (
                "author",
                "title",
                "description",
                "image",
            )
        }),

        ("Recipe Details", {
            "fields": (
                "category",
                "difficulty",
                "servings",
            )
        }),

        ("Cooking Time", {
            "fields": (
                "prep_time",
                "cook_time",
                "total_time",
            )
        }),

        ("Recipe Content", {
            "fields": (
                "ingredients",
                "instructions",
            )
        }),

        ("Status", {
            "fields": (
                "is_featured",
                "created_at",
                "updated_at",
            )
        }),
    )


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = (
        "recipe",
        "user",
        "score",
        "created_at",
    )

    list_filter = (
        "score",
        "created_at",
    )

    search_fields = (
        "recipe__title",
        "user__username",
    )

    ordering = (
        "-created_at",
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "recipe",
        "user",
        "created_at",
    )

    list_filter = (
        "created_at",
    )

    search_fields = (
        "recipe__title",
        "user__username",
        "text",
    )

    ordering = (
        "-created_at",
    )


@admin.register(SavedRecipe)
class SavedRecipeAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "recipe",
        "saved_at",
    )

    list_filter = (
        "saved_at",
    )

    search_fields = (
        "user__username",
        "recipe__title",
    )

    ordering = (
        "-saved_at",
    )