from rest_framework import serializers
from .models import TblCategories, TblBrands, TblSubCategories, TblModels, TblMainAds

base_url = 'http://pasal.yantrashala.com/api/v1'


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

    class Meta:
        model = TblSubCategories
        fields = ('sub_category_id', 'sub_category_name', 'category', 'detail_url')

    def get_detail_url(self, obj):
        return base_url + '/sub-category/' + str(obj.sub_category_id)


class CategorySingleSerializer(serializers.ModelSerializer):
    inner_list_url = serializers.SerializerMethodField()

    class Meta:
        model = TblCategories
        fields = ('category_id', 'category_name', 'inner_list_url')

    def get_inner_list_url(self, obj):
        return base_url + '/category/' + str(obj.category_id) + '/sub-category/list'


class MainAdsListSerializer(serializers.ModelSerializer):
    model = serializers.ReadOnlyField(source="model.model_name")
    sub_category = serializers.ReadOnlyField(source="sub_category.sub_category_name")
    customer = serializers.ReadOnlyField(source="customer.email.email")
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = TblMainAds
        fields = ('main_ads_id', 'ad_run_days', 'ad_title', 'added_date', 'description',
        'expired', 'expiry_date', 'featured', 'price', 'price_negotiable', 'view_count',
        'customer', 'sub_category', 'model', 'detail_url')

    def get_detail_url(self, obj):
        return base_url + '/main-ads/' + str(obj.main_ads_id)


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


class MainAdsDetailSerializer(serializers.ModelSerializer):
    specs = serializers.SerializerMethodField()
    customer = serializers.ReadOnlyField(source="customer.email.email")
    model = serializers.ReadOnlyField(source="model.model_name")
    sub_category = serializers.ReadOnlyField(source="sub_category.sub_category_name")

    class Meta:
        model = TblMainAds
        # fields = TblMainAds._meta.get_fields()
        fields = ('main_ads_id', 'ad_run_days', 'ad_title', 'added_date', 'description',
        'expired', 'expiry_date', 'featured', 'price', 'price_negotiable', 'view_count',
        'customer', 'sub_category', 'model', 'specs')

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
                datas = field.related_model.objects.filter(main_ads=obj).values()
                data[field.related_model._meta.model_name.replace("tbl", "")] = datas[0]
        # objects = [{f.related_model._meta.model_name.replace("tbl", "") : f.related_model.objects.filter(main_ads=obj).values() for f in related_models}]
        return data
