# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class TblAccessorySpec(models.Model):
    gender = models.CharField(max_length=255, blank=True, null=True)
    main_ads = models.ForeignKey('TblMainAds', models.DO_NOTHING, unique=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_accessory_spec'


class TblBrands(models.Model):
    brand_id = models.AutoField(primary_key=True)
    activate = models.TextField()  # This field type is a guess.
    brand_name = models.CharField(max_length=255, blank=True, null=True)
    facebook_link = models.CharField(max_length=255, blank=True, null=True)
    google_plus_link = models.CharField(max_length=255, blank=True, null=True)
    instagram_link = models.CharField(max_length=255, blank=True, null=True)
    twitter_link = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_brands'


class TblBusinessSpec(models.Model):
    included_in_price = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    main_ads = models.ForeignKey('TblMainAds', models.DO_NOTHING, unique=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_business_spec'


class TblCarSpec(models.Model):
    color = models.CharField(max_length=255, blank=True, null=True)
    engine = models.CharField(max_length=255, blank=True, null=True)
    features = models.TextField(blank=True, null=True)
    fuel = models.CharField(max_length=255, blank=True, null=True)
    kilometers = models.IntegerField()
    make_year = models.IntegerField()
    transmission = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    main_ads = models.ForeignKey('TblMainAds', models.DO_NOTHING, unique=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_car_spec'


class TblCars(models.Model):
    car_id = models.AutoField(primary_key=True)
    car_name = models.CharField(max_length=255, blank=True, null=True)
    color = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    engine = models.IntegerField()
    features = models.TextField(blank=True, null=True)
    fuel = models.CharField(max_length=255, blank=True, null=True)
    make_year = models.IntegerField()
    price = models.FloatField()
    transmission = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    brand = models.ForeignKey(TblBrands, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_cars'


class TblCategories(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_categories'


class TblClothingSpec(models.Model):
    color = models.CharField(max_length=255, blank=True, null=True)
    size = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    main_ads = models.ForeignKey('TblMainAds', models.DO_NOTHING, unique=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_clothing_spec'


class TblCommonSpec(models.Model):
    spec_condition = models.CharField(max_length=255, blank=True, null=True)
    used_for = models.CharField(max_length=255, blank=True, null=True)
    main_ads = models.ForeignKey('TblMainAds', models.DO_NOTHING, unique=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_common_spec'


class TblCustomer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    added_date = models.DateTimeField()
    name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    verified = models.IntegerField()
    email = models.ForeignKey('TblUsers', models.DO_NOTHING, db_column='email', unique=True, blank=True, null=True)
    city_name = models.CharField(max_length=255)
    area_location = models.CharField(max_length=255, blank=True, null=True)
    street_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_customer'


class TblDelivery(models.Model):
    delivery_area = models.CharField(max_length=255, blank=True, null=True)
    delivery_charges = models.CharField(max_length=255, blank=True, null=True)
    home_delivery = models.CharField(max_length=255, blank=True, null=True)
    main_ads = models.ForeignKey('TblMainAds', models.DO_NOTHING, unique=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_delivery'


class TblHandsetSpec(models.Model):
    back_camera = models.CharField(max_length=255, blank=True, null=True)
    cpu_core = models.CharField(max_length=255, blank=True, null=True)
    features = models.TextField(blank=True, null=True)
    front_camera = models.CharField(max_length=255, blank=True, null=True)
    internal_storage = models.CharField(max_length=255, blank=True, null=True)
    ownership = models.CharField(max_length=255, blank=True, null=True)
    ram = models.CharField(max_length=255, blank=True, null=True)
    screen_size = models.CharField(max_length=255, blank=True, null=True)
    sim_slot = models.CharField(max_length=255, blank=True, null=True)
    smartphone_os = models.CharField(max_length=255, blank=True, null=True)
    main_ads = models.ForeignKey('TblMainAds', models.DO_NOTHING, unique=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_handset_spec'


class TblHousings(models.Model):
    housing_id = models.AutoField(primary_key=True)
    added_date = models.DateField(blank=True, null=True)
    appliances = models.CharField(max_length=255, blank=True, null=True)
    area = models.IntegerField()
    available = models.CharField(max_length=255, blank=True, null=True)
    bathroom = models.IntegerField()
    bedroom = models.IntegerField()
    cooling = models.CharField(max_length=255, blank=True, null=True)
    dates = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    flooring = models.CharField(max_length=255, blank=True, null=True)
    heating = models.CharField(max_length=255, blank=True, null=True)
    housing_name = models.CharField(max_length=255, blank=True, null=True)
    laundry = models.CharField(max_length=255, blank=True, null=True)
    others = models.CharField(max_length=255, blank=True, null=True)
    parking = models.CharField(max_length=255, blank=True, null=True)
    pets = models.CharField(max_length=255, blank=True, null=True)
    price = models.FloatField()
    purpose = models.CharField(max_length=255, blank=True, null=True)
    rent_per_sqft = models.FloatField()
    type = models.CharField(max_length=255, blank=True, null=True)
    unit_floor = models.IntegerField()
    brand = models.ForeignKey(TblBrands, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_housings'


class TblLaptopSpec(models.Model):
    battery = models.CharField(max_length=255, blank=True, null=True)
    features = models.TextField(blank=True, null=True)
    hdd = models.CharField(max_length=255, blank=True, null=True)
    processor = models.CharField(max_length=255, blank=True, null=True)
    processor_generation = models.CharField(max_length=255, blank=True, null=True)
    ram = models.IntegerField()
    screen_size = models.IntegerField()
    screen_type = models.CharField(max_length=255, blank=True, null=True)
    video_card = models.CharField(max_length=255, blank=True, null=True)
    main_ads = models.ForeignKey('TblMainAds', models.DO_NOTHING, unique=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_laptop_spec'


class TblMainAds(models.Model):
    main_ads_id = models.AutoField(primary_key=True)
    ad_run_days = models.IntegerField()
    ad_title = models.CharField(max_length=255)
    added_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    expired = models.TextField()  # This field type is a guess.
    expiry_date = models.DateField(blank=True, null=True)
    featured = models.TextField()  # This field type is a guess.
    price = models.BigIntegerField()
    price_negotiable = models.CharField(max_length=255, blank=True, null=True)
    view_count = models.IntegerField()
    customer = models.ForeignKey(TblCustomer, models.DO_NOTHING, blank=True, null=True)
    sub_category = models.ForeignKey('TblSubCategories', models.DO_NOTHING, blank=True, null=True)
    model = models.ForeignKey('TblModels', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_main_ads'


class TblModels(models.Model):
    model_id = models.AutoField(primary_key=True)
    model_name = models.CharField(max_length=255, blank=True, null=True)
    sub_category = models.ForeignKey('TblSubCategories', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_models'


class TblMonitorSpec(models.Model):
    size = models.IntegerField()
    type = models.CharField(max_length=255, blank=True, null=True)
    main_ads = models.ForeignKey(TblMainAds, models.DO_NOTHING, unique=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_monitor_spec'


class TblMotocycleSpec(models.Model):
    anchal = models.CharField(max_length=255, blank=True, null=True)
    engine = models.IntegerField()
    features = models.TextField(blank=True, null=True)
    kilometers = models.IntegerField()
    lot_no = models.IntegerField()
    make_year = models.IntegerField()
    mileage = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    main_ads = models.ForeignKey(TblMainAds, models.DO_NOTHING, unique=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_motocycle_spec'


class TblNetworkingEquipmentSpec(models.Model):
    type = models.CharField(max_length=255, blank=True, null=True)
    main_ads = models.ForeignKey(TblMainAds, models.DO_NOTHING, unique=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_networking_equipment_spec'


class TblPictures(models.Model):
    picture_name = models.CharField(max_length=255, blank=True, null=True)
    car = models.ForeignKey(TblCars, models.DO_NOTHING, blank=True, null=True)
    housing = models.ForeignKey(TblHousings, models.DO_NOTHING, blank=True, null=True)
    main_ads = models.ForeignKey(TblMainAds, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_pictures'


class TblPrinterSpec(models.Model):
    features = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    main_ads = models.ForeignKey(TblMainAds, models.DO_NOTHING, unique=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_printer_spec'


class TblQuestions(models.Model):
    question_id = models.AutoField(primary_key=True)
    asked_on = models.DateField(blank=True, null=True)
    question_comment = models.CharField(max_length=255, blank=True, null=True)
    asked_by = models.ForeignKey(TblCustomer, models.DO_NOTHING, db_column='asked_by', blank=True, null=True, related_name='asked_questions')
    asked_to = models.ForeignKey(TblCustomer, models.DO_NOTHING, db_column='asked_to', blank=True, null=True)
    main_ads = models.ForeignKey(TblMainAds, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_questions'


class TblRealestateSpec(models.Model):
    access_road = models.CharField(max_length=255, blank=True, null=True)
    area = models.CharField(max_length=255, blank=True, null=True)
    bathroom = models.IntegerField()
    bedroom = models.IntegerField()
    built_up = models.IntegerField()
    features = models.TextField(blank=True, null=True)
    floors = models.IntegerField()
    furnishing = models.CharField(max_length=255, blank=True, null=True)
    land_size = models.IntegerField()
    livingroom = models.IntegerField()
    property_location = models.CharField(max_length=255, blank=True, null=True)
    property_type = models.CharField(max_length=255, blank=True, null=True)
    water_supply = models.CharField(max_length=255, blank=True, null=True)
    main_ads = models.ForeignKey(TblMainAds, models.DO_NOTHING, unique=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_realestate_spec'


class TblReplies(models.Model):
    reply_id = models.AutoField(primary_key=True)
    replied = models.TextField()  # This field type is a guess.
    reply_comment = models.CharField(max_length=255, blank=True, null=True)
    question = models.ForeignKey(TblQuestions, models.DO_NOTHING, unique=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_replies'


class TblShoesSpec(models.Model):
    color = models.CharField(max_length=255, blank=True, null=True)
    size = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    main_ads = models.ForeignKey(TblMainAds, models.DO_NOTHING, unique=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_shoes_spec'


class TblSoftwareSpec(models.Model):
    genre = models.CharField(max_length=255, blank=True, null=True)
    main_ads = models.ForeignKey(TblMainAds, models.DO_NOTHING, unique=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_software_spec'


class TblSportSpec(models.Model):
    body = models.CharField(max_length=255, blank=True, null=True)
    gear = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    wheel_size = models.CharField(max_length=255, blank=True, null=True)
    main_ads = models.ForeignKey(TblMainAds, models.DO_NOTHING, unique=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_sport_spec'


class TblStorageSpec(models.Model):
    size = models.CharField(max_length=255, blank=True, null=True)
    storage_type = models.CharField(max_length=255, blank=True, null=True)
    main_ads = models.ForeignKey(TblMainAds, models.DO_NOTHING, unique=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_storage_spec'


class TblSubCategories(models.Model):
    sub_category_id = models.AutoField(primary_key=True)
    sub_category_name = models.CharField(max_length=255, blank=True, null=True)
    category = models.ForeignKey(TblCategories, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_sub_categories'


class TblTabletSpec(models.Model):
    camera = models.CharField(max_length=255, blank=True, null=True)
    connectivity = models.CharField(max_length=255, blank=True, null=True)
    features = models.TextField(blank=True, null=True)
    internal_storage = models.IntegerField()
    os = models.CharField(max_length=255, blank=True, null=True)
    ram = models.CharField(max_length=255, blank=True, null=True)
    screen = models.CharField(max_length=255, blank=True, null=True)
    main_ads = models.ForeignKey(TblMainAds, models.DO_NOTHING, unique=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_tablet_spec'


class TblTravelSpec(models.Model):
    duration = models.CharField(max_length=255, blank=True, null=True)
    inclusion = models.CharField(max_length=255, blank=True, null=True)
    rating = models.IntegerField()
    main_ads = models.ForeignKey(TblMainAds, models.DO_NOTHING, unique=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_travel_spec'


class TblUserRoles(models.Model):
    user_id = models.AutoField(primary_key=True)
    role = models.CharField(max_length=255, blank=True, null=True)
    email = models.ForeignKey('TblUsers', models.DO_NOTHING, db_column='email', unique=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_user_roles'


class TblUsers(models.Model):
    email = models.CharField(primary_key=True, max_length=100)
    enabled = models.TextField()  # This field type is a guess.
    password = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'tbl_users'


class TblWarranty(models.Model):
    warranty_includes = models.CharField(max_length=255, blank=True, null=True)
    warranty_period = models.CharField(max_length=255, blank=True, null=True)
    warranty_type = models.CharField(max_length=255, blank=True, null=True)
    main_ads = models.ForeignKey(TblMainAds, models.DO_NOTHING, unique=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_warranty'


class TblWishlist(models.Model):
    customer = models.ForeignKey(TblCustomer, models.DO_NOTHING, blank=True, null=True)
    main_ads = models.ForeignKey(TblMainAds, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_wishlist'
