# app1/api_views.py

from django.db.models import Count, Q
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models       import Listing, Tag, Category, Profile
from .serializers  import (
    ListingSerializer,
    TagSerializer,
    CategorySerializer,
    ProfileSerializer,
)

class ListingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset           = Listing.objects.prefetch_related("tags","category")
    serializer_class   = ListingSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=True, url_path="similar")
    def similar(self, request, pk=None):
        listing = self.get_object()
        qs = (
            Listing.objects
                   .filter(
                      Q(category=listing.category) |
                      Q(tags__in=listing.tags.all())
                   )
                   .exclude(pk=listing.pk)
                   .annotate(
                      common_tags=Count(
                        "tags",
                        filter=Q(tags__in=listing.tags.all())
                      )
                   )
                   .order_by("-common_tags", "-created_at")[:10]
        )
        return Response(self.get_serializer(qs, many=True).data)

class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset         = Tag.objects.all()
    serializer_class = TagSerializer

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset         = Category.objects.all()
    serializer_class = CategorySerializer

class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    """
    /api/profiles/                  → list of profiles
    /api/profiles/{pk}/             → detail of one profile
    /api/profiles/{pk}/recommendations/ → your “for you” suggestions
    """
    queryset           = Profile.objects.prefetch_related("favorites__tags").all()
    serializer_class   = ProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=["get"], url_path="recommendations")
    def recommendations(self, request, pk=None):
        profile = self.get_object()
        tag_ids = profile.favorites.values_list("tags__id", flat=True)
        qs = (
            Listing.objects
                   .filter(tags__in=tag_ids)
                   .exclude(favorited_by=profile)
                   .annotate(
                      match_count=Count(
                        "tags",
                        filter=Q(tags__in=tag_ids)
                      )
                   )
                   .order_by("-match_count", "-created_at")[:10]
        )
        return Response(ListingSerializer(qs, many=True, context={"request":request}).data)
