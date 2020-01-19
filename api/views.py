from django.shortcuts import render
from .models import TblCategories, TblBrands, TblSubCategories, TblModels, TblMainAds
from rest_framework import viewsets
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView,\
    RetrieveUpdateDestroyAPIView, RetrieveAPIView
from .serializers import CategorySerializer, CategorySingleSerializer, BrandSerializer, SubCategorySerializer, \
    ProductModelSerializer, MainAdsSerializer
    

class CategoryViewSet(ListAPIView):
    serializer_class = CategorySerializer
    queryset = TblCategories.objects.all()


class CategorySingleViewSet(RetrieveAPIView):
    serializer_class = CategorySingleSerializer
    
    def get_object(self):
        return TblCategories.objects.get(category_id=self.kwargs.get('category_id'))


"""
    For listing all subcategories
"""
class SubCategoryViewSet(ListAPIView):
    serializer_class = SubCategorySerializer
    queryset = TblSubCategories.objects.all()


class SubCategorySingleViewSet(RetrieveAPIView):
    serializer_class = SubCategorySerializer

    def get_object(self):
        return TblSubCategories.objects.get(sub_category_id=self.kwargs.get('sub_category_id'))
    

class ProductModelViewSet(viewsets.ModelViewSet):
    serializer_class = ProductModelSerializer
    queryset = TblModels.objects.all()


class BrandViewSet(viewsets.ModelViewSet):
    serializer_class = BrandSerializer
    queryset = TblBrands.objects.all()


class MainAdsViewSet(viewsets.ModelViewSet):
    serializer_class = MainAdsSerializer
    queryset = TblMainAds.objects.all()