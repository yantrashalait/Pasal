from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import permissions
from rest_framework.views import APIView

from django.shortcuts import render, get_object_or_404
from .models import TblCategories, TblBrands, TblSubCategories, TblModels, TblMainAds, \
TblHousings, TblCars, TblCustomer, TblUsers, TblUserRoles, TblCommonSpec
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView,\
    RetrieveUpdateDestroyAPIView, RetrieveAPIView, CreateAPIView
from .serializers import CategorySerializer, CategorySingleSerializer, BrandSerializer, \
    SubCategoryListSerializer, SubCategoryDetailSerializer, ProductModelListSerializer, \
    ProductModelDetailSerializer, MainAdsListSerializer, MainAdsDetailSerializer, AllCategorySerializer,\
    HousingListSerializer, HousingDetailSerializer, CarListSerializer, CarDetailSerializer, CustomerDetailSerializer,\
    RegisterSerializer, MainAdsCreateSerializer, MainAdsCommonSpecSerializer, GenericSpecificationSerializer
from django.db import transaction
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK

from django.contrib.auth import get_user_model
from datetime import datetime

from django.db.models import Q
from django.apps import apps

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


class RegisterViewSet(APIView):
    def post(self, request, format=None):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # create role for user
            TblUserRoles.objects.create(email=user, role="ROLE_USER")

            # create user profile
            TblCustomer.objects.create(
                email=user, 
                added_date=datetime.now(),
                name="", 
                phone="",
                verified=False, 
                city_name="")

            if user:
                return Response({
                    'status': True,
                    'email': user.email
                }, status=HTTP_200_OK)
        else:
            return Response({
                'status': False,
                'data': serializer.errors
            }, status=HTTP_400_BAD_REQUEST)


class FeaturedMainAdsViewSet(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MainAdsListSerializer
    queryset = TblMainAds.objects.filter(featured=True, expired=False) # check expiry date

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            'status': True,
            'data': serializer.data
        }, status=HTTP_200_OK)


class HousingListViewSet(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = HousingListSerializer

    def get_queryset(self, *args, **kwargs):
        return TblHousings.objects.all()

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            'status': True,
            'data': serializer.data
        }, status=HTTP_200_OK)


class HousingDetailViewSet(RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = HousingDetailSerializer

    def get_object(self, *args, **kwargs):
        return get_object_or_404(TblHousings, housing_id=self.kwargs.get('housing_id'))

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response({
            'status': True,
            'data': serializer.data
        }, status=HTTP_200_OK)


class CarListViewSet(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CarListSerializer

    def get_queryset(self, *args, **kwargs):
        return TblCars.objects.all()

    def get(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            'status': True,
            'data': serializer.data
        }, status=HTTP_200_OK)


class CarDetailViewSet(RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CarDetailSerializer

    def get_object(self, *args, **kwargs):
        return get_object_or_404(TblCars, car_id=self.kwargs.get('car_id'))

    def get(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response({
            'status': True,
            'data': serializer.data
        }, status=HTTP_200_OK)


class AllCategoryListViewSet(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AllCategorySerializer
    queryset = TblCategories.objects.all()

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            'status': True,
            'data': serializer.data
        }, status=HTTP_200_OK)


class CategoryViewSet(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CategorySerializer
    queryset = TblCategories.objects.all()

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            'status': True,
            'data': serializer.data
        }, status=HTTP_200_OK)


class CategorySingleViewSet(RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
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
    permission_classes = [permissions.IsAuthenticated]
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
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return TblSubCategories.objects.get(sub_category_id=self.kwargs.get('sub_category_id'))

    def get(self, request, *args, **kwargs):
        serializer = SubCategoryDetailSerializer(instance=self.get_object())
        return Response({
            'status': True,
            'data': serializer.data
        }, status=HTTP_200_OK)


class ModelListViewSet(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
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
    permission_classes = [permissions.IsAuthenticated]
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
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BrandSerializer
    queryset = TblBrands.objects.all()


class MainAdsViewSet(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
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
    permission_classes = [permissions.IsAuthenticated]
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


class SearchViewSet(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MainAdsListSerializer

    def get_queryset(self, *args, **kwargs):
        key = self.request.GET.get('search', '')
        return TblMainAds.objects.filter(Q(ad_title__icontains=key)|Q(sub_category__sub_category_name__icontains=key)|Q(sub_category__category__category_name__icontains=key))

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            'status': True,
            'data': serializer.data
        }, status=HTTP_200_OK)


class UserProfileViewSet(RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CustomerDetailSerializer

    def get_object(self, *args, **kwargs):
        return TblCustomer.objects.get(email=self.request.user)

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response({
            'status': True,
            'data': serializer.data
        }, status=HTTP_200_OK)
    
    def put(self, request, *args, **kawrgs):
        serializer = self.get_serializer(self.get_object(), data=request.data)
        if not serializer.is_valid():
            return Response({
                'status': False,
                'data': serializer.errors
            })
        self.perform_update(serializer)
        return Response({
            'status': True,
            'msg': 'Updated Successfully',
            'data': serializer.data
        })


class MainAdsCreateViewSet(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MainAdsCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'status': False,
                'data': serializer.errors
            }, status=HTTP_400_BAD_REQUEST)

        if 'category_id' in self.request.GET:
            category = TblCategories.objects.get(category_id=self.request.GET.get('category_id', 1))
        if 'model_id' in self.request.GET:
            model = TblModels.objects.get(model_id=self.request.GET.get('model_id', 1))
        else:
            model = None
        if 'sub_category_id' in self.request.GET:
            sub_category = TblSubCategories.objects.get(sub_category_id=self.request.GET.get('sub_category_id', 1))
        else:
            sub_category = None
            
        customer = TblCustomer.objects.get(email=self.request.user)

        main_ads_kwargs = serializer.validated_data
        main_ads = TblMainAds(**main_ads_kwargs)
        if model:
            main_ads.model = model
        if sub_category:
            main_ads.sub_category = sub_category
        
        main_ads.customer = customer
        main_ads.added_date = datetime.now()
        main_ads.expired = False
        main_ads.view_count = 0
        main_ads.save()

        serializer = self.get_serializer(main_ads)
        
        return Response({
            'status': True,
            'msg': 'Added Successfully',
            'data': serializer.data
        }, status=HTTP_200_OK)
    
    def get_serializer_context(self):
        return {'model_name': self.request.GET.get("model_name")}


class MainAdsCommonSpecAddViewSet(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MainAdsCommonSpecSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                'status': False,
                'data': serializer.errors
            }, status=HTTP_400_BAD_REQUEST)
        main_ads = TblMainAds.objects.get(main_ads_id=self.kwargs.get('main_ads_id'))
        common_spec_kwargs = serializer.validated_data
        common_spec = TblCommonSpec(**common_spec_kwargs)
        common_spec.main_ads = main_ads
        common_spec.save()

        serializer = self.get_serializer(common_spec)

        return Response({
            'status': True,
            'msg': 'Added Successully',
            'data': serializer.data
        }, status=HTTP_200_OK)
    
    def get_serializer_context(self):
        return {'model_name': self.request.GET.get("model_name")}



class MainAdsCommonSpecEditViewSet(RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MainAdsCommonSpecSerializer

    def get_object(self, *args, **kwargs):
        return TblCommonSpec.objects.get(id=self.kwargs.get('common_id'))
    
    def get(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response({
            'status': True,
            'data': serializer.data
        }, status=HTTP_200_OK)
    
    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object(), data=request.data)
        if not serializer.is_valid():
            return Response({
                'status': False,
                'data': serializer.errors
            }, status=HTTP_400_BAD_REQUEST)
        self.perform_update(serializer)
        return Response({
            'status': True,
            'msg': 'Updated Successfully',
            'data': serializer.data
        })


class MainAdsSpecificationCreateViewSet(CreateAPIView):
    def get_serializer_class(self):
        model = apps.get_model('api', self.request.GET.get('model_name'))
        GenericSpecificationSerializer.Meta.model = model
        GenericSpecificationSerializer.Meta.fields = "__all__"
        return GenericSpecificationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'status': False,
                'data': serializer.errors
            }, status=HTTP_400_BAD_REQUEST)
        print(self.request.POST)