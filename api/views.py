from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from django.shortcuts import render, get_object_or_404
from .models import TblCategories, TblBrands, TblSubCategories, TblModels, TblMainAds
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView,\
    RetrieveUpdateDestroyAPIView, RetrieveAPIView
from .serializers import CategorySerializer, CategorySingleSerializer, BrandSerializer, \
    SubCategoryListSerializer, SubCategoryDetailSerializer, ProductModelListSerializer, \
    ProductModelDetailSerializer, MainAdsListSerializer, MainAdsDetailSerializer, AllCategorySerializer
from django.db import transaction
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK

from django.contrib.auth import get_user_model

from .models import TblUsers
from datetime import datetime

User = get_user_model()

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny, ))
def login(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    if email is None and password is None:
        return Response(
            {'error': 'Please provide both email and password.'},
            status=HTTP_400_BAD_REQUEST)
    user = authenticate(email=email, password=password)

    if not user:
        return Response(
            {'error': 'Invalid Credentials.'},
            status = HTTP_404_NOT_FOUND,
        )
    token, created = Token.objects.get_or_create(user=user)
    return Response(
        {
            'token': token.key
        },
        status=HTTP_200_OK
    )


class FeaturedMainAdsViewSet(ListAPIView):
    serializer_class = MainAdsListSerializer
    queryset = TblMainAds.objects.filter(featured=True, expired=False) # check expiry date

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            'status': True,
            'data': serializer.data
        }, status=HTTP_200_OK)


class AllCategoryListViewSet(ListAPIView):
    serializer_class = AllCategorySerializer
    queryset = TblCategories.objects.all()

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            'status': True,
            'data': serializer.data
        }, status=HTTP_200_OK)


class CategoryViewSet(ListAPIView):
    serializer_class = CategorySerializer
    queryset = TblCategories.objects.all()

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            'status': True,
            'data': serializer.data
        }, status=HTTP_200_OK)


class CategorySingleViewSet(RetrieveAPIView):
    serializer_class = CategorySingleSerializer

    def get_object(self):
        return get_object_or_404(TblCategories, category_id=self.kwargs.get('category_id'))

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response({
            'status': True,
            'data': serializer.data
        }, status=HTTP_200_OK)


"""
    For listing subcategories
"""
class SubCategoryViewSet(ListAPIView):
    serializer_class = SubCategoryListSerializer

    def get_queryset(self, *args, **kwargs):
        return TblSubCategories.objects.filter(category=self.kwargs.get('category_id'))

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            'status': True,
            'data': serializer.data
        }, status=HTTP_200_OK)


class SubCategorySingleViewSet(RetrieveAPIView):

    def get_object(self):
        return TblSubCategories.objects.get(sub_category_id=self.kwargs.get('sub_category_id'))

    def get(self, request, *args, **kwargs):
        serializer = SubCategoryDetailSerializer(instance=self.get_object())
        return Response({
            'status': True,
            'data': serializer.data
        }, status=HTTP_200_OK)


class ModelListViewSet(ListAPIView):
    serializer_class = ProductModelListSerializer

    def get_queryset(self, *args, **kwargs):
        sub_cat = get_object_or_404(TblSubCategories, sub_category_id=self.kwargs.get('sub_category_id'))
        return TblModels.objects.filter(sub_category=sub_cat)

    def get(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            'status': True,
            'data': serializer.data
        }, status=HTTP_200_OK)


class ModelDetailViewSet(RetrieveAPIView):
    serializer_class = ProductModelDetailSerializer

    def get_object(self, *args, **kwargs):
        return get_object_or_404(TblModels, model_id=self.kwargs.get('model_id'))

    def get(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response({
            'status': True,
            'data': serializer.data
        }, status=HTTP_200_OK)


class BrandViewSet(viewsets.ModelViewSet):
    serializer_class = BrandSerializer
    queryset = TblBrands.objects.all()


class MainAdsViewSet(ListAPIView):
    serializer_class = MainAdsListSerializer

    def get_queryset(self, *args, **kwargs):
        sub_cat = get_object_or_404(TblSubCategories, sub_category_id=self.kwargs.get('sub_category_id'))
        return TblMainAds.objects.filter(sub_category=sub_cat)

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            'status': True,
            'data': serializer.data
        }, status=HTTP_200_OK)


class MainAdsDetailViewSet(RetrieveAPIView):
    serializer_class = MainAdsDetailSerializer

    def get_object(self, *args, **kwargs):
        main_ads = get_object_or_404(TblMainAds, main_ads_id=self.kwargs.get('main_ads_id'))
        return main_ads

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response({
            'status': True,
            'data': serializer.data
        }, status=HTTP_200_OK)
