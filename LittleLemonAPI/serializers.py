from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
import bleach
from decimal import Decimal
from django.contrib.auth.models import User
from .models import MenuItem, Category, Rating

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','slug','title']

class MenuItemSerializer(serializers.HyperlinkedModelSerializer):
    stock = serializers.IntegerField(source='inventory', min_value=0)
    price = serializers.DecimalField(max_digits=6, decimal_places=2, min_value=2)
    price_after_tax = serializers.SerializerMethodField(method_name = 'calculate_tax')
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    title = serializers.CharField(
        max_length=255, 
        validators = [UniqueValidator(queryset=MenuItem.objects.all())]
        )

    def validate_title(self, value):
        return bleach.clean(value)
    class Meta:
        model = MenuItem
        fields = ['id','title','price','stock','price_after_tax','category','category_id']

    def calculate_tax(self, product:MenuItem):
        return product.price * Decimal(1.1)
    

class RatingSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset = User.objects.all(),
        default = serializers.CurrentUserDefault()
    )

    class Meta:
        model = Rating
        fields = ['user','menuitem_id','rating']

    validators = [
        UniqueTogetherValidator(
            queryset=Rating.objects.all(), 
            fields = ['user','menuitem_id','rating']
        )
    ]

    extra_kwargs = {
        'rating': {'max_value': 5, 'min_value': 0},
    }
    