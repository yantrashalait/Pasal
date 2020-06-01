import os
import io
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import *
from django.core.exceptions import ValidationError
from PIL import Image


server_url = "http://bhumijaonline.com:8001"

base_url = 'http://bhumijaonline.com:8001/api/v1'

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, required=True)
    password1 = serializers.CharField(max_length=255, required=True)
    password2 = serializers.CharField(max_length=255, required=True)

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise ValidationError('Passwords must match.')
        return data

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise ValidationError("User with this email already exists.")
        return email

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password1']
        user = User.objects.create(email=email, enabled=False, password=password)
        return user


class AllCategorySerializer(serializers.ModelSerializer):
    sub_categories = serializers.SerializerMethodField()

    class Meta:
        model = TblCategories
        fields = ('category_id', 'category_name', 'sub_categories')

    def get_sub_categories(self, obj):
        sub_categories = TblSubCategories.objects.filter(category=obj).values()
        for item in sub_categories:
            fields=[]
            related_models = []
            main_ads = TblMainAds.objects.filter(sub_category__sub_category_id=item['sub_category_id'])
            if main_ads:
                obj1 = main_ads[0]
                for model in obj1._meta.get_fields():
                    if model.get_internal_type() == "ForeignKey":
                        try:
                            if model.field.get_internal_type() == "ForeignKey":
                                related_models.append(model)
                        except:
                            pass
                for field in related_models:
                    if field.related_model._meta.model_name.find(item['sub_category_name'].lower()) != -1 or field.related_model.objects.filter(main_ads=obj1).exists():
                        if field.related_model._meta.model_name == "tblquestions":
                            continue
                        if field.related_model._meta.model_name == "tblpictures":
                            continue
                        if field.related_model._meta.model_name == "tblwishlist":
                            continue

                        model_name = field.related_model._meta.model_name

                        if "spec"in model_name and model_name != "tblcommonspec":
                            item['model_name'] = model_name
        return sub_categories


class CategorySerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = TblCategories
        fields = ('category_id', 'category_name', 'detail_url')

    def get_detail_url(self, obj):
        return base_url + '/category/' + str(obj.category_id)


class SubCategoryListSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()
    category = serializers.ReadOnlyField(source="category.category_name")
    model_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = TblSubCategories
        fields = ('sub_category_id', 'sub_category_name', 'category', 'detail_url', 'model_name')

    def get_detail_url(self, obj):
        return base_url + '/sub-category/' + str(obj.sub_category_id)

    def get_model_name(self, obj):
        fields=[]
        related_models = []
        main_ads = TblMainAds.objects.filter(sub_category=obj)
        if main_ads:
            obj1 = main_ads[0]
            for model in obj1._meta.get_fields():
                if model.get_internal_type() == "ForeignKey":
                    try:
                        if model.field.get_internal_type() == "ForeignKey":
                            related_models.append(model)
                    except:
                        pass
            for field in related_models:
                if field.related_model.objects.filter(main_ads=obj1).exists():
                    if field.related_model._meta.model_name == "tblquestions":
                        continue
                    if field.related_model._meta.model_name == "tblpictures":
                        continue
                    if field.related_model._meta.model_name == "tblwishlist":
                        continue

                    model_name = field.related_model._meta.model_name

                    if "spec"in model_name and model_name != "tblcommonspec":
                        return model_name


class CategorySingleSerializer(serializers.ModelSerializer):
    inner_list_url = serializers.SerializerMethodField()

    class Meta:
        model = TblCategories
        fields = ('category_id', 'category_name', 'inner_list_url')

    def get_inner_list_url(self, obj):
        return base_url + '/category/' + str(obj.category_id) + '/sub-category/list'


class MainAdsPictures(serializers.ModelSerializer):
    class Meta:
        model = TblPictures
        fields = '__all__'


class CustomerDetailSerializer(serializers.ModelSerializer):
    verified = serializers.ReadOnlyField()
    customer_id = serializers.ReadOnlyField()
    added_date = serializers.ReadOnlyField()
    email = serializers.ReadOnlyField(source="email.email")

    class Meta:
        model = TblCustomer
        fields = '__all__'
        extra_kwargs = {
            'name': {'required': True},
            'phone': {'required': True},
        }


class RepliesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblReplies
        fields= ('reply_id', 'replied', 'reply_comment')


class QuestionsSerializer(serializers.ModelSerializer):
    asked_by = CustomerDetailSerializer()
    asked_to = CustomerDetailSerializer()
    tblreplies_set = RepliesSerializer(many=True)

    class Meta:
        model = TblQuestions
        fields = ('question_id', 'asked_on', 'question_comment', 'asked_by', 'asked_to', 'tblreplies_set')


class MainAdsListSerializer(serializers.ModelSerializer):
    model = serializers.ReadOnlyField(source="model.model_name")
    sub_category = serializers.ReadOnlyField(source="sub_category.sub_category_name")
    customer = serializers.ReadOnlyField(source="customer.email.email")
    detail_url = serializers.SerializerMethodField()
    pictures = serializers.SerializerMethodField()
    model_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = TblMainAds
        fields = ('main_ads_id', 'ad_run_days', 'ad_title', 'added_date', 'description',
        'expired', 'expiry_date', 'featured', 'price', 'price_negotiable', 'view_count',
        'customer', 'sub_category', 'model', 'detail_url', 'pictures', 'model_name')

    def get_detail_url(self, obj):
        return base_url + '/main-ads/' + str(obj.main_ads_id)

    def get_pictures(self, obj):
        pictures = TblPictures.objects.filter(main_ads=obj).values('id', 'picture_name')
        for item in pictures:
            picture_media_url = os.path.join(settings.MEDIA_ROOT, "mainads/" + item['picture_name'])
            item['picture_url'] = server_url + picture_media_url
        return pictures

    def get_model_name(self, obj):
        fields=[]
        related_models = []
        for model in obj._meta.get_fields():
            if model.get_internal_type() == "ForeignKey":
                try:
                    if model.field.get_internal_type() == "ForeignKey":
                        related_models.append(model)
                except:
                    pass
        for field in related_models:
            if field.related_model.objects.filter(main_ads=obj).exists():
                if field.related_model._meta.model_name == "tblquestions":
                    continue
                if field.related_model._meta.model_name == "tblpictures":
                    continue
                if field.related_model._meta.model_name == "tblwishlist":
                    continue

                model_name = field.related_model._meta.model_name

                if "spec"in model_name and model_name != "tblcommonspec":
                    return model_name


class ProductModelListSerializer(serializers.ModelSerializer):
    sub_category = serializers.ReadOnlyField(source='sub_category.sub_category_name')
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = TblModels
        fields = ('model_id', 'model_name', 'sub_category', 'detail_url')

    def get_detail_url(self, obj):
        return base_url + '/model/' + str(obj.model_id)


class SubCategoryDetailSerializer(serializers.ModelSerializer):
    category = serializers.ReadOnlyField(source="category.category_name")
    inner_list_url = serializers.SerializerMethodField()

    class Meta:
        model = TblSubCategories
        fields = ('sub_category_id', 'sub_category_name', 'category', 'inner_list_url')

    def get_inner_list_url(self, obj):
        if obj.tblmainads_set.all():
            return base_url + '/sub-category/' + str(obj.sub_category_id) + '/main-ads/list'
        else:
            return base_url + '/sub-category/' + str(obj.sub_category_id) + '/model/list'


class ProductModelDetailSerializer(serializers.ModelSerializer):
    sub_category = serializers.ReadOnlyField(source="sub_category.sub_category_name")
    tblmainads_set = MainAdsListSerializer(many=True, read_only=True)

    class Meta:
        model = TblModels
        fields = ('model_id', 'model_name', 'sub_category', 'tblmainads_set')


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = TblBrands
        fields = '__all__'


class PictureSerializer(serializers.ModelSerializer):

    class Meta:
        model = TblPictures
        fields = "__all__"


class MainAdsDetailSerializer(serializers.ModelSerializer):
    specs = serializers.SerializerMethodField(read_only=True)
    customer = CustomerDetailSerializer(read_only=True)
    model = serializers.ReadOnlyField(source="model.model_name")
    sub_category = serializers.ReadOnlyField(source="sub_category.sub_category_name")
    tblquestions_set = QuestionsSerializer(many=True, read_only=True)
    pictures = serializers.SerializerMethodField(read_only=True)
    model_name = serializers.SerializerMethodField(read_only=True)
    main_ads_id = serializers.ReadOnlyField()
    added_date = serializers.ReadOnlyField()
    expired = serializers.BooleanField(read_only=True)
    expiry_date = serializers.ReadOnlyField()
    view_count = serializers.ReadOnlyField()

    class Meta:
        model = TblMainAds
        fields = ('main_ads_id', 'ad_run_days', 'ad_title', 'added_date', 'description',
        'expired', 'expiry_date', 'featured', 'price', 'price_negotiable', 'view_count',
        'customer', 'sub_category', 'model', 'specs', 'tblquestions_set', 'pictures', 'model_name')

    def get_pictures(self, obj):
        pictures = TblPictures.objects.filter(main_ads=obj).values('id', 'picture_name')
        for item in pictures:
            picture_media_url = os.path.join(settings.MEDIA_ROOT, "mainads/" + item['picture_name'])
            item['picture_url'] = server_url + picture_media_url
        return pictures

    def get_specs(self, obj):
        fields=[]
        related_models = []
        for model in obj._meta.get_fields():
            if model.get_internal_type() == "ForeignKey":
                try:
                    if model.field.get_internal_type() == "ForeignKey":
                        related_models.append(model)
                except:
                    pass
        data = {}
        for field in related_models:
            if field.related_model.objects.filter(main_ads=obj).exists():
                if field.related_model._meta.model_name == "tblquestions":
                    continue
                if field.related_model._meta.model_name == "tblpictures":
                    continue
                if field.related_model._meta.model_name == "tblwishlist":
                    continue
                datas = field.related_model.objects.filter(main_ads=obj).values()

                model_name = field.related_model._meta.model_name

                if "spec"in model_name and model_name != "tblcommonspec":
                    print(field.related_model)
                if field.related_model._meta.model_name == "tblaccessoryspec":
                    data["Accessory Specification"] = datas
                if field.related_model._meta.model_name == "tblbusinessspec":
                    data["Business Specification"] = datas
                if field.related_model._meta.model_name == "tblcarspec":
                    data["Car Specification"] = datas
                if field.related_model._meta.model_name == "tblclothingspec":
                    data["Clothing Specification"] = datas
                if field.related_model._meta.model_name == "tblcommonspec":
                    data["Common Specification"] = datas
                if field.related_model._meta.model_name == "tbldelivery":
                    data["Delivery Details"] = datas
                if field.related_model._meta.model_name == "tblhandsetspec":
                    data["Handset Specification"] = datas
                if field.related_model._meta.model_name == "tbllaptopspec":
                    data["Laptop Specification"] = datas
                if field.related_model._meta.model_name == "tblmonitorspec":
                    data["Monitor Specification"] = datas
                if field.related_model._meta.model_name == "tblmotocyclespec":
                    data["MotorCycle Specification"] = datas
                if field.related_model._meta.model_name == "tblnetworkingequipmentspec":
                    data["Networking Equipment Specification"] = datas
                if field.related_model._meta.model_name == "tblprinterspec":
                    data["Printer Specification"] = datas
                if field.related_model._meta.model_name == "tblrealestatespec":
                    data["Real Estate Specification"] = datas
                if field.related_model._meta.model_name == "tblshoesspec":
                    data["Shoes Specification"] = datas
                if field.related_model._meta.model_name == "tblsoftwarespec":
                    data["Software Specification"] = datas
                if field.related_model._meta.model_name == "tblsportspec":
                    data["Sport Specification"] = datas
                if field.related_model._meta.model_name == "tblstoragespec":
                    data["Storage Specification"] = datas
                if field.related_model._meta.model_name == "tbltabletspec":
                    data["Tablet Specification"] = datas
                if field.related_model._meta.model_name == "tblwarranty":
                    data["Warranty Details"] = datas

                # data[field.related_model._meta.model_name.replace("tbl", "")] = datas
        # objects = [{f.related_model._meta.model_name.replace("tbl", "") : f.related_model.objects.filter(main_ads=obj).values() for f in related_models}]
        return data

    def get_model_name(self, obj):
        fields=[]
        related_models = []
        for model in obj._meta.get_fields():
            if model.get_internal_type() == "ForeignKey":
                try:
                    if model.field.get_internal_type() == "ForeignKey":
                        related_models.append(model)
                except:
                    pass
        for field in related_models:
            if field.related_model.objects.filter(main_ads=obj).exists():
                if field.related_model._meta.model_name == "tblquestions":
                    continue
                if field.related_model._meta.model_name == "tblpictures":
                    continue
                if field.related_model._meta.model_name == "tblwishlist":
                    continue

                model_name = field.related_model._meta.model_name

                if model_name:
                    if "spec"in model_name and model_name != "tblcommonspec":
                        return model_name

        sub_category = obj.sub_category
        main_ads = TblMainAds.objects.filter(sub_category=sub_category)
        if main_ads:
            obj1 = main_ads[0]
            for model in obj1._meta.get_fields():
                if model.get_internal_type() == "ForeignKey":
                    try:
                        if model.field.get_internal_type() == "ForeignKey":
                            related_models.append(model)
                    except:
                        pass
            for field in related_models:
                if field.related_model.objects.filter(main_ads=obj1).exists():
                    if field.related_model._meta.model_name == "tblquestions":
                        continue
                    if field.related_model._meta.model_name == "tblpictures":
                        continue
                    if field.related_model._meta.model_name == "tblwishlist":
                        continue

                    model_name = field.related_model._meta.model_name

                    if "spec"in model_name and model_name != "tblcommonspec":
                        return model_name


class HousingListSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()
    brand = serializers.ReadOnlyField(source="brand.brand_id")
    pictures = serializers.SerializerMethodField()
    brand_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = TblHousings
        fields = ('housing_id', 'brand', 'area', 'available', 'description', 'housing_name', 'rent_per_sqft', 'type', 'detail_url', 'pictures', 'brand_name')

    def get_detail_url(self, obj):
        return base_url + '/housing/detail/' + str(obj.housing_id)

    def get_pictures(self, obj):
        pictures = TblPictures.objects.filter(housing=obj).values('id', 'picture_name')
        for item in pictures:
            picture_media_url = os.path.join(settings.MEDIA_ROOT, "housing/" + obj.brand.brand_name + "/" + item['picture_name'])
            item['picture_url'] = server_url + picture_media_url
        return pictures

    def get_brand_name(self, obj):
        return obj.brand.brand_name


class HousingDetailSerializer(serializers.ModelSerializer):
    brand = serializers.ReadOnlyField(source="brand.brand_id")
    pictures = serializers.SerializerMethodField(read_only=True)
    housing_id = serializers.ReadOnlyField()
    brand_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = TblHousings
        fields = ('housing_id', 'brand', 'added_date', 'appliances', 'area', 'available',
        'bathroom', 'bedroom', 'cooling', 'dates', 'description', 'flooring', 'heating',
        'housing_name', 'laundry', 'others', 'parking', 'pets', 'price', 'purpose',
        'rent_per_sqft', 'type', 'unit_floor', 'pictures', 'brand_name')

    def get_pictures(self, obj):
        pictures = TblPictures.objects.filter(housing=obj).values('id', 'picture_name')
        for item in pictures:
            picture_media_url = os.path.join(settings.MEDIA_ROOT, "housing/" + obj.brand.brand_name + "/" + item['picture_name'])
            item['picture_url'] = server_url + picture_media_url
        return pictures

    def get_brand_name(self, obj):
        return obj.brand.brand_name


class CarAddSerializer(serializers.ModelSerializer):
    car_id = serializers.ReadOnlyField()
    pictures = PictureSerializer(many=True, required=False)

    class Meta:
        model = TblCars
        fields = ("car_id", 'car_name', 'color', 'description', 'engine', 'features',
        'fuel', 'make_year', 'price', 'transmission', 'type', 'brand', 'pictures')

    def create(self, validated_data):
        car = TblCars.objects.create(**validated_data)
        pictures_new = validated_data.get('pictures', [])
        for picture in pictures_new:
            file = io.BytesIO(picture.file.read())
            file.seek(0)
            image = Image.open(file)
            picture_name = picture._name.replace(" ", "_")
            path_to_save = os.path.join(settings.MEDIA_ROOT, "car/", car.brand.brand_name)
            path_to_save = os.path.join(path_to_save, picture_name)
            image.save(path_to_save)
            TblPictures.objects.update_or_create(car=car, picture_name=picture_name)
        return car

    def update(self, instance, validated_data):
        pictures_new = validated_data.get('pictures', [])
        for picture in pictures_new:
            file = io.BytesIO(picture.file.read())
            file.seek(0)
            image = Image.open(file)
            picture_name = picture._name.replace(" ", "_")
            path_to_save = os.path.join(settings.MEDIA_ROOT, "car/", instance.brand.brand_name)
            path_to_save = os.path.join(path_to_save, picture_name)
            image.save(path_to_save)
            TblPictures.objects.update_or_create(car=instance, picture_name=picture_name)
        return super(CarAddSerializer, self).update(instance, validated_data)


class HousingAddSerializer(serializers.ModelSerializer):
    housing_id = serializers.ReadOnlyField()
    pictures = PictureSerializer(many=True, required=False)

    class Meta:
        model = TblHousings
        fields = "__all__"

    def create(self, validated_data):
        housing = TblHousings.objects.create(**validated_data)
        housing.added_date = datetime.now().date
        pictures_new = validated_data.get('pictures', [])
        for picture in pictures_new:
            file = io.BytesIO(picture.file.read())
            file.seek(0)
            image = Image.open(file)
            picture_name = picture._name.replace(" ", "_")
            path_to_save = os.path.join(settings.MEDIA_ROOT, "housing/", housing.brand.brand_name)
            path_to_save = os.path.join(path_to_save, picture_name)
            image.save(path_to_save)
            TblPictures.objects.update_or_create(housing=housing, picture_name=picture_name)
        return housing

    def update(self, instance, validated_data):
        pictures_new = validated_data.get('pictures', [])
        for picture in pictures_new:
            file = io.BytesIO(picture.file.read())
            file.seek(0)
            image = Image.open(file)
            picture_name = picture._name.replace(" ", "_")
            path_to_save = os.path.join(settings.MEDIA_ROOT, "housing/", instance.brand.brand_name)
            path_to_save = os.path.join(path_to_save, picture_name)
            image.save(path_to_save)
            TblPictures.objects.update_or_create(housing=instance, picture_name=picture_name)
        return super(HousingAddSerializer, self).update(instance, validated_data)


class CarListSerializer(serializers.ModelSerializer):
    brand = serializers.ReadOnlyField(source="brand.brand_id")
    detail_url = serializers.SerializerMethodField()
    pictures = serializers.SerializerMethodField()
    brand_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = TblCars
        fields = ('car_id', 'car_name', 'color', 'description', 'engine', 'make_year',
        'price', 'type', 'brand', 'detail_url', 'pictures', 'brand_name')

    def get_detail_url(self, obj):
        return base_url + '/car/detail/' + str(obj.car_id)

    def get_pictures(self, obj):
        pictures = TblPictures.objects.filter(car=obj).values('id', 'picture_name')
        for item in pictures:
            picture_media_url = os.path.join(settings.MEDIA_ROOT, "car/" + obj.brand.brand_name + "/" + item['picture_name'])
            item['picture_url'] = server_url + picture_media_url
        return pictures

    def get_brand_name(self, obj):
        return obj.brand.brand_name


class CarDetailSerializer(serializers.ModelSerializer):
    brand = serializers.ReadOnlyField(source="brand.brand_id")
    car_id = serializers.ReadOnlyField()
    pictures = serializers.SerializerMethodField(read_only=True)
    brand_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = TblCars
        fields = ('car_id', 'car_name', 'color', 'description', 'engine', 'features',
        'fuel', 'make_year', 'price', 'transmission', 'type', 'brand', 'pictures', 'brand_name')

    def get_pictures(self, obj):
        pictures = TblPictures.objects.filter(car=obj).values('id', 'picture_name')
        for item in pictures:
            picture_media_url = os.path.join(settings.MEDIA_ROOT, "car/" + obj.brand.brand_name + "/" + item['picture_name'])
            item['picture_url'] = server_url + picture_media_url
        return pictures

    def get_brand_name(self, obj):
        return obj.brand.brand_name


class MainAdsCreateSerializer(serializers.ModelSerializer):
    main_ads_id = serializers.ReadOnlyField()
    added_date = serializers.ReadOnlyField()
    expired = serializers.BooleanField(read_only=True)
    view_count = serializers.ReadOnlyField()
    customer = serializers.ReadOnlyField(source="customer.email.email")
    sub_category = serializers.ReadOnlyField(source="sub_category.sub_category_name")
    model = serializers.ReadOnlyField(source="model.model_name")
    model_name = serializers.SerializerMethodField(read_only=True)
    expiry_date = serializers.ReadOnlyField()
    pictures = PictureSerializer(many=True, required=False)

    class Meta:
        model = TblMainAds
        fields = ('main_ads_id', 'added_date', 'expired', 'view_count', 'customer',
        'sub_category', 'model', 'ad_run_days', 'ad_title', 'description', 'expiry_date',
        'featured', 'price', 'price_negotiable', 'model_name', 'pictures')
        extra_kwargs = {
            'ad_run_days': {'required': True},
            'ad_title': {'required': True},
            'description': {'required': True},
            'featured': {'required': True},
            'price': {'required': True},
            'price_negotiable': {'required': True},
            }

    def get_model_name(self, obj):
        return  self.context.get("model_name")


class MainAdsCommonSpecSerializer(serializers.ModelSerializer):
    main_ads = serializers.ReadOnlyField(source="main_ads.main_ads_id")
    model_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = TblCommonSpec
        fields = '__all__'

    def get_model_name(self, obj):
        model_name = self.context.get("model_name")
        return model_name


class GenericSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = None


class MainAdsWarrantySerializer(serializers.ModelSerializer):
    main_ads = serializers.ReadOnlyField(source="main_ads.main_ads_id")

    class Meta:
        model = TblWarranty
        fields = "__all__"


class MainAdsDeliverySerializer(serializers.ModelSerializer):
    main_ads = serializers.ReadOnlyField(source="main_ads.main_ads_id")

    class Meta:
        model = TblDelivery
        fields = "__all__"
