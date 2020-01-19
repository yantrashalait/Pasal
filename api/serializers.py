from rest_framework import serializers
from .models import TblCategories, TblBrands, TblSubCategories, TblModels, TblMainAds

base_url = 'localhost:8000/api/v1'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TblCategories
        fields = '__all__'


class CategorySingleSerializer(serializers.ModelSerializer):
    sub_categories = serializers.SerializerMethodField()

    class Meta:
        model = TblCategories
        fields = ('category_id', 'category_name', 'sub_categories')
    
    def get_sub_categories(self, obj):
        sub_cat = TblSubCategories.objects.filter(category=obj).values('sub_category_name', 'sub_category_id')
        for item in sub_cat:
            item['detail_url'] = base_url + '/sub-category/' + str(item['sub_category_id'])
        return sub_cat


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TblSubCategories
        fields = '__all__'


class ProductModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblModels
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblBrands
        fields = '__all__'


class MainAdsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblMainAds
        fields = '__all__'