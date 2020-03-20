from django.urls import path
from rest_framework.authtoken import views as restviews
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register(r'brand', views.BrandViewSet, basename='brand')


urlpatterns = [
    path('api-auth-token', views.login),

    # for index page
    path('featured/main-ads/list', views.FeaturedMainAdsViewSet.as_view(), name='featured-main-ads'),
    path('housing/list', views.HousingListViewSet.as_view(), name="housing-list"),
    path('housing/detail/<int:housing_id>', views.HousingDetailViewSet.as_view(), name="housing-detail"),
    path('car/list', views.CarListViewSet.as_view(), name="car-list"),
    path('car/detail/<int:car_id>', views.CarDetailViewSet.as_view(), name="car-detail"),

    # for all categories in category list page
    path('category/all', views.AllCategoryListViewSet.as_view(), name="category-all"),

    path('category/list', views.CategoryViewSet.as_view(), name='category-list'),
    path('category/<int:category_id>', views.CategorySingleViewSet.as_view(), name='cat-single'),
    path('category/<int:category_id>/sub-category/list', views.SubCategoryViewSet.as_view(), name='sub-cat-list'),
    path('sub-category/<int:sub_category_id>', views.SubCategorySingleViewSet.as_view(), name='sub-cat-single'),
    path('sub-category/<int:sub_category_id>/main-ads/list', views.MainAdsViewSet.as_view(), name="main-ads-list"),
    path('sub-category/<int:sub_category_id>/model/list', views.ModelListViewSet.as_view(), name="model-list"),
    path('model/<int:model_id>', views.ModelDetailViewSet.as_view(), name="model-detail"),

    path('main-ads/<int:main_ads_id>', views.MainAdsDetailViewSet.as_view(), name="main-ads-list"),

    path('search', views.SearchViewSet.as_view(), name="search"),

    path('user/profile/', views.UserProfileViewSet.as_view(), name="user-profile"),
]

urlpatterns += router.urls
