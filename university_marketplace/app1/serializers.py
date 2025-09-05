from rest_framework import serializers
from .models import Listing, Category, Tag, Profile

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]

class ListingSerializer(serializers.ModelSerializer):
    tags      = TagSerializer(many=True, read_only=True)
    category  = CategorySerializer(read_only=True)
    seller    = serializers.StringRelatedField()

    class Meta:
        model = Listing
        fields = [
            "id", "title", "description", "price",
            "tags", "category", "seller", "created_at",
        ]
class ProfileSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField(source='user.user', read_only=True)

    favorites = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
        source='favorites'     
    )

    class Meta:
        model  = Profile
        fields = ['id', 'user', 'favorites']