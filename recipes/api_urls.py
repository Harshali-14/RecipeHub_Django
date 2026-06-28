from rest_framework.routers import DefaultRouter
from .api_views import RecipeViewSet

router = DefaultRouter()
router.register(r'recipes', RecipeViewSet, basename='recipe')

urlpatterns = router.urls