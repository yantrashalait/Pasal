from django.urls import path
from rest_framework.authtoken import views as restviews
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register(r'models', views.ProductModelViewSet, basename='models')
router.register(r'brand', views.BrandViewSet, basename='brand')
router.register(r'mainads', views.MainAdsViewSet, basename='mainads')



urlpatterns = [
    path('category/list/', views.CategoryViewSet.as_view(), name='category-list'),
    path('category/<int:category_id>/', views.CategorySingleViewSet.as_view(), name='cat-single'),
    path('<int:category_id>/sub-category/list/', views.SubCategoryViewSet.as_view(), name='sub-cat-list'),
    path('sub-category/<int:sub_category_id>/', views.SubCategorySingleViewSet.as_view(), name='sub-cat-single'),
]

urlpatterns += router.urls