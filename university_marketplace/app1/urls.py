from django.urls import path, include
from . import views
from .views import healthz

urlpatterns = [
    path("",                           views.home,            name="home"),

    path("about/",                     views.about,           name="about"),
    path("server_info/",               views.server_info,     name="server_info"),    
    path("signup/",                    views.signup,          name="signup"),
    path('join/',   views.signup, name='join'),
    path("upload/",                    views.create_listing,  name="upload"),
    path("item/<int:pk>/",             views.detail_listing,  name="detail"),
    path("item/<int:pk>/appointment/", views.create_appointment, name="upload_appointment"),
    path("item/<int:pk>/report/",      views.report_listing,  name="report_listing"),
    path("item/<int:pk>/reviews/",     views.listing_reviews, name="listing_reviews"),
    path("item/<int:pk>/delete/",      views.delete_listing,  name="delete_listing"),
    path("item/<int:pk>/chat/",        views.chat_fragment,   name="chat_fragment"), 
    path("notifications/mark_read/",   views.mark_read,       name="mark_read"),
    path("notifications/count/",       views.get_unread_count, name="get_unread_count"),
    path("appointments/<int:pk>/complete/", views.complete_appointment, name="complete_appointment"),
    path("item/<int:pk>/favorite/", views.toggle_favorite, name="toggle_favorite"),
    path("wishlist/", views.my_wishlist, name="my_wishlist"),
    path("recommendations/", views.my_recommendations, name="recommendations"),
    path("my-listings/",   views.my_listings,    name="my_listings"),
    path("manage-listings/",views.manage_listings, name="manage_listings"),
    path("reported/", views.reported_listings, name="reported_listings"),
    path("api/", include("rest_framework.urls")),
    path("item/<int:pk>/add-images/", views.add_images, name="add_images"),
    path('profile/', views.profile_edit, name='profile_edit'),
    path("healthz/", healthz, name="healthz"),
]
