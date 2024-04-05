from django.contrib.auth.models import Group, User
from rest_framework import serializers

from dronerental.rentalservice.models import Category, Brand, UAV, RentalTransaction


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description')

    def create(self, validated_data):
        return super().create(validated_data)


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('id', 'name', 'description')

    def create(self, validated_data):
        return super().create(validated_data)


class UAVSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    brand = BrandSerializer()

    class Meta:
        model = UAV
        fields = '__all__'

    def create(self, validated_data):
        return super().create(validated_data)


class RentalTransactionSerializer(serializers.ModelSerializer):
    start_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    end_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    uav = UAVSerializer()
    username = serializers.SerializerMethodField()

    class Meta:
        model = RentalTransaction
        fields = '__all__'

    def get_username(self, obj):
        return obj.user.username
