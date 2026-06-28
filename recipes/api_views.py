from rest_framework import viewsets, permissions, filters
from .models import Recipe
from .serializers import RecipeSerializer
from .permissions import IsRecipeOwnerOrReadOnly

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all().order_by("-created_at")
    serializer_class = RecipeSerializer

    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    search_fields = [
        "title",
        "description",
        "ingredients",
        "category",
    ]

    ordering_fields = [
        "created_at",
        "prep_time",
        "cook_time",
    ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
    
    
def get_permissions(self):
    if self.action in ["list", "retrieve"]:
        permission_classes = [permissions.AllowAny]
    else:
        permission_classes = [
            permissions.IsAuthenticated,
            IsRecipeOwnerOrReadOnly,
        ]
    return [permission() for permission in permission_classes]