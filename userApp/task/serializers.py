from rest_framework import serializers
from django.contrib.auth.models import User
from .models import product


class CreateUserSerializer(serializers.ModelSerializer):
    """Validate the public fields accepted when a user registers."""

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        """Create a Django user so its password is stored using Django hashing."""
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
        )

        return user


class CreateProductSerializers(serializers.ModelSerializer):
    """Serialize product fields for creation and partial updates."""

    class Meta:
        model = product
        fields = "__all__"

        # Ownership and timestamps are managed by the server, not the request.
        read_only_fields = [ "created_by", "created_at", "updated_at",]



class getProductSerializers(serializers.ModelSerializer):
    """Expose the product fields used by list and detail responses."""

    class Meta:
        model = product
        fields = ["id",  "product_name", "product_category", "product_price"]
    