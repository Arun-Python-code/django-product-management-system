from rest_framework import serializers
from django.contrib.auth.models import User
from .models import product


class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
        )

        return user

class CreateProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = product
        fields = "__all__"

        read_only_fields = [ "created_by", "created_at", "updated_at",]



class getProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = product
        fields = ["id",  "product_name", "product_category", "product_price"]
    