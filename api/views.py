from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import permissions
from rest_framework.views import APIView

from django.shortcuts import render, get_object_or_404
from .models import TblCategories, TblBrands, TblSubCategories, TblModels, TblMainAds, \
TblHousings, TblCars, TblCustomer, TblUsers, TblUserRoles, TblCommonSpec, TblWarranty, TblDelivery
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView,\
    RetrieveUpdateDestroyAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView
from .serializers import CategorySerializer, CategorySingleSerializer, BrandSerializer, \
    SubCategoryListSerializer, SubCategoryDetailSerializer, ProductModelListSerializer, \
    ProductModelDetailSerializer, MainAdsListSerializer, MainAdsDetailSerializer, AllCategorySerializer,\
    HousingListSerializer, HousingDetailSerializer, CarListSerializer, CarDetailSerializer, CustomerDetailSerializer,\
    RegisterSerializer, MainAdsCreateSerializer, MainAdsCommonSpecSerializer, GenericSpecificationSerializer, \
    MainAdsWarrantySerializer, MainAdsDeliverySerializer, CarAddSerializer, HousingAddSerializer
from django.db import transaction
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK

from django.contrib.auth import get_user_model
from datetime import datetime, timedelta

from django.db.models import Q
from django.apps import apps

User = get_user_model()

from .permissions import IsOwnerOrReadOnly

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
    customer = TblCustomer.objects.get(email=user)
    token, created = Token.objects.get_or_create(user=user)
    return Response(
        {
            'token': token.key,
            'user_id': customer.customer_id
        },
        status=HTTP_200_OK
    )


class RegisterViewSet(APIView):
    def post(self, request, format=None):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.enabled = True
            user.save()

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


class HousingDetailViewSet(RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, *args, **kwargs):
        return get_object_or_404(TblHousings, housing_id=self.kwargs.get('housing_id'))

    def get(self, request, *args, **kwargs):
        serializer = HousingDetailSerializer(self.get_object())
        return Response({
            'status': True,
            'data': serializer.data
        }, status=HTTP_200_OK)
    
    def put(self, *args, **kwargs):
        serializer = HousingAddSerializer(self.get_object(), data=self.request.data)
        if not serializer.is_valid():
            return Response({
                'status': False,
                'msg': serializer.errors
            }, status=HTTP_400_BAD_REQUEST)
        self.perform_update(serializer)
        serializer = HousingDetailSerializer(self.get_object())
        return Response({
            'status': True,
            'msg': 'Successfully updated',
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


class CarDetailViewSet(RetrieveUpdateAPIView):
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

    def put(self, *args, **kwargs):
        serializer = CarAddSerializer(self.get_object(), data=self.request.data)
        if not serializer.is_valid():
            return Response({
                'status': False,
                'msg': serializer.errors
            }, status=HTTP_400_BAD_REQUEST)
        self.perform_update(serializer)
        serializer = CarDetailSerializer(self.get_object())
        return Response({
            'status': True,
            'msg': 'Successfully updated',
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
        return TblMainAds.objects.filter(Q(sub_category=sub_cat)|Q(model__sub_category=sub_cat))

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            'status': True,
            'data': serializer.data
        }, status=HTTP_200_OK)


class MainAdsDetailViewSet(RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = MainAdsDetailSerializer

    def get_object(self, *args, **kwargs):
        main_ads = get_object_or_404(TblMainAds, main_ads_id=self.kwargs.get('main_ads_id'))
        self.check_object_permissions(self.request, main_ads)
        return main_ads

    def get(self, request, *args, **kwargs):
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
        
        main_ads = self.get_object()

        if 'ad_run_days' in serializer.validated_data:
            run_days = serializer.validated_data['ad_run_days']
            today = datetime.now()
            run_until = timedelta(days=int(run_days))

            expiry_date_time = today + run_until
            expiry_date = expiry_date_time.date()
            main_ads.ad_run_days = run_days
            main_ads.expiry_date = expiry_date

            if today.date() > expiry_date:
                main_ads.expired = True
            else:
                main_ads.expired = False
        
        if 'ad_title' in serializer.validated_data:
            main_ads.ad_title = serializer.validated_data['ad_title']
        if 'description' in serializer.validated_data:
            main_ads.description = serializer.validated_data['description']
        if 'featured' in serializer.validated_data:
            main_ads.featured = serializer.validated_data['featured']
        if 'price' in serializer.validated_data:
            main_ads.price = serializer.validated_data['price']
        if 'price_negotiable' in serializer.validated_data:
            main_ads.price_negotiable = serializer.validated_data['price_negotiable']
        
        main_ads.save()

        serializer = self.get_serializer(main_ads)

        return Response({
            'status': True,
            'msg': 'Updated successfully.',
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
        
        run_days = serializer.validated_data['ad_run_days']
        today = datetime.now()
        run_until = timedelta(days=int(run_days))

        expiry_date_time = today + run_until
        expiry_date = expiry_date_time.date()
        main_ads.expiry_date = expiry_date

        if today.date() > expiry_date:
            main_ads.expired = True
        else:
            main_ads.expired = False
        
        main_ads.customer = customer
        main_ads.added_date = datetime.now()
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


class MainAdsCommonSpecAddViewSet(APIView):

    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def post(self, request, *args, **kwargs):
        main_ads = TblMainAds.objects.get(main_ads_id=self.kwargs.get('main_ads_id'))
        self.check_object_permissions(self.request, main_ads)

        serializer = MainAdsCommonSpecSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                'status': False,
                'data': serializer.errors
            }, status=HTTP_400_BAD_REQUEST)
        
        common_spec_kwargs = serializer.validated_data
        common_spec = TblCommonSpec(**common_spec_kwargs)
        common_spec.main_ads = main_ads
        common_spec.save()

        serializer = MainAdsCommonSpecSerializer(common_spec)

        return Response({
            'status': True,
            'msg': 'Added Successully',
            'data': serializer.data
        }, status=HTTP_200_OK)
    
    def get_object(self, *args, **kwargs):
        main_ads = TblMainAds.objects.get(main_ads_id=self.kwargs.get('main_ads_id'))
        self.check_object_permissions(self.request, main_ads)
        return get_object_or_404(TblCommonSpec, main_ads=main_ads)
    
    def put(self, request, *args, **kwargs):
        serializer = MainAdsCommonSpecSerializer(self.get_object(), data=request.data)
        if not serializer.is_valid():
            return Response({
                'status': False,
                'data': serializer.errors
            }, status=HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({
            'status': True,
            'msg': 'Updated Successfully',
            'data': serializer.data
        }, status=HTTP_200_OK)
    
    def get_serializer_context(self):
        return {'model_name': self.request.GET.get("model_name")}



class MainAdsCommonSpecDetailViewSet(RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = MainAdsCommonSpecSerializer

    def get_object(self, *args, **kwargs):
        main_ads = TblMainAds.objects.get(main_ads_id=self.kwargs.get('main_ads_id'))
        return get_object_or_404(TblCommonSpec, main_ads=main_ads)
    
    def get(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response({
            'status': True,
            'data': serializer.data
        }, status=HTTP_200_OK)
        
    def get_serializer_context(self):
        return {'model_name': self.request.GET.get("model_name")}


class MainAdsSpecificationCreateViewSet(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_serializer_class(self):
        model = apps.get_model('api', self.request.GET.get('model_name'))
        GenericSpecificationSerializer.Meta.model = model
        GenericSpecificationSerializer.Meta.fields = "__all__"
        return GenericSpecificationSerializer

    def post(self, request, *args, **kwargs):
        main_ads = TblMainAds.objects.get(main_ads_id=self.kwargs.get('main_ads_id'))
        self.check_object_permissions(self.request, main_ads)

        _serializer = self.get_serializer_class()

        serializer = _serializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                'status': False,
                'data': serializer.errors
            }, status=HTTP_400_BAD_REQUEST)
        
        spec = serializer.save()
        spec.main_ads = main_ads
        spec.save()

        return Response({
            'status': True,
            'msg': 'Created Successfully.',
            'data': serializer.data
        }, status=HTTP_200_OK)
    
    def put(self, request, *args, **kwargs):
        _serializer = self.get_serializer_class()

        serializer = _serializer(self.get_object(), data=request.data)
        if not serializer.is_valid():
            return Response({
                'status': False,
                'data': serializer.errors
            }, status=HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response({
            'status': True,
            'msg': 'Updated successfully.',
            'data': serializer.data
        }, status=HTTP_200_OK)
    
    def get_object(self, *args, **kwargs):
        model = apps.get_model("api", self.request.GET.get('model_name'))
        main_ads = TblMainAds.objects.get(main_ads_id=self.kwargs.get("main_ads_id"))
        self.check_object_permissions(self.request, main_ads)
        return get_object_or_404(model, main_ads=main_ads)
    

class MainAdsSpecificationDetailViewSet(RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_serializer_class(self):
        model = apps.get_model('api', self.request.GET.get('model_name'))
        GenericSpecificationSerializer.Meta.model = model
        GenericSpecificationSerializer.Meta.fields = "__all__"
        return GenericSpecificationSerializer
    
    def get_object(self, *args, **kwargs):
        model = apps.get_model("api", self.request.GET.get('model_name'))
        main_ads = TblMainAds.objects.get(main_ads_id=self.kwargs.get("main_ads_id"))
        return get_object_or_404(model, main_ads=main_ads)

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response({
            'status': True,
            'data': serializer.data
        }, status=HTTP_200_OK)


class MainAdsWarrantyCreateViewSet(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def post(self, request, *args, **kwargs):
        main_ads = TblMainAds.objects.get(main_ads_id=self.kwargs.get('main_ads_id'))
        self.check_object_permissions(self.request, main_ads)

        serializer = MainAdsWarrantySerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'status': False,
                'msg': serializer.errors
            }, status=HTTP_400_BAD_REQUEST)
        warranty = serializer.save()
        
        warranty.main_ads = main_ads
        warranty.save()
        return Response({
            'status': True,
            'msg': 'Created Successfully',
            'data': serializer.data
        }, status=HTTP_200_OK)

    def get_object(self, *args, **kwargs):
        main_ads = TblMainAds.objects.get(main_ads_id=self.kwargs.get('main_ads_id'))
        self.check_object_permissions(self.request, main_ads)
        return get_object_or_404(TblWarranty, main_ads=main_ads)

    def put(self, request, *args, **kwargs):
        serializer = MainAdsWarrantySerializer(self.get_object(), data=request.data)
        if not serializer.is_valid():
            return Response({
                'status': False,
                'data': serializer.errors
            }, status=HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({
            'status': True,
            'msg': 'Updated successfully',
            'data': serializer.data
        }, status=HTTP_200_OK)


class MainAdsWarrantyDetailViewSet(RetrieveAPIView):
    serializer_class = MainAdsWarrantySerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_object(self, *args, **kwargs):
        main_ads = TblMainAds.objects.get(main_ads_id=self.kwargs.get('main_ads_id'))
        return get_object_or_404(TblWarranty, main_ads=main_ads)

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response({
            'status': True,
            'data': serializer.data
        }, status=HTTP_200_OK)


class MainAdsDeliveryCreateViewSet(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def post(self, request, *args, **kwargs):
        main_ads = TblMainAds.objects.get(main_ads_id=self.kwargs.get('main_ads_id'))
        self.check_object_permissions(self.request, main_ads)

        serializer = MainAdsDeliverySerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'status': False,
                'data': serializer.errors
            }, status=HTTP_400_BAD_REQUEST)
        
        delivery = serializer.save()
        
        delivery.main_ads = main_ads
        delivery.save()
        return Response({
            'status': True,
            'msg': 'Created successfully',
            'data': serializer.data
        }, status=HTTP_200_OK)
    
    def get_object(self, *args, **kwargs):
        main_ads = TblMainAds.objects.get(main_ads_id=self.kwargs.get('main_ads_id'))
        self.check_object_permissions(self.request, main_ads)
        return get_object_or_404(TblDelivery, main_ads=main_ads)
    
    def put(self, request, *args, **kwargs):
        serializer = MainAdsDeliverySerializer(self.get_object(), data=request.data)
        if not serializer.is_valid():
            return Response({
                'status': False,
                'data': serializer.errors
            }, status=HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response({
            'status': True,
            'msg': 'Updated successfully',
            'data': serializer.data
        })


class MainAdsDeliveryDetailViewSet(RetrieveAPIView):
    serializer_class = MainAdsDeliverySerializer
    permissions_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_object(self, *args, **kwargs):
        main_ads = TblMainAds.objects.get(main_ads_id=self.kwargs.get('main_ads_id'))
        return get_object_or_404(TblDelivery, main_ads=main_ads)
    
    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response({
            'status': True,
            'data': serializer.data
        }, status=HTTP_200_OK)


class UserAdsViewSet(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MainAdsListSerializer

    def get_queryset(self, *args, **kwargs):
        return TblMainAds.objects.filter(customer__email=self.request.user)
    
    def get(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            'status': True,
            'data': serializer.data
        }, status=HTTP_200_OK)


class BrandListViewSet(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BrandSerializer

    def get_queryset(self, *args, **kwargs):
        return TblBrands.objects.all()
    
    def get(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            'status': True,
            'data': serializer.data
        }, status=HTTP_200_OK)
    

class CarAddViewSet(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CarAddSerializer

    def post(self, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        if not serializer.is_valid():
            return Response({
                'status': False,
                'data': serializer.errors
            }, status=HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({
            'status': True,
            'msg': 'Created successfully'
        }, status=HTTP_200_OK)


class HousingAddViewSet(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = HousingAddSerializer

    def post(self, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        if not serializer.is_valid():
            return Response({
                'status': False,
                'data': serializer.errors
            }, status=HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        return Response({
            'status': True,
            'msg':' Created successfully',
        }, status=HTTP_200_OK)