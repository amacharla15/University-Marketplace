# university_marketplace/urls.py

from django.contrib import admin
from django.urls    import path, include
from django.conf    import settings
from django.conf.urls.static import static
from django.views.decorators.csrf  import ensure_csrf_cookie
from django.views.decorators.cache import never_cache
from django.contrib.auth import views as auth_views

from university_marketplace.app1 import views as app_views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from university_marketplace.app1.api_views import (ListingViewSet, TagViewSet, CategoryViewSet, ProfileViewSet,)

router = DefaultRouter()
router.register(r"listings", ListingViewSet)
router.register(r"tags", TagViewSet)
router.register(r"categories", CategoryViewSet)
router.register(r'profiles',   ProfileViewSet,   basename='profile')

urlpatterns = [
    path('admin/', admin.site.urls),


  path("password_reset/", 
       auth_views.PasswordResetView.as_view(
        template_name="registration/password_reset_form.html",
        email_template_name="registration/password_reset_email.html",
        subject_template_name="registration/password_reset_subject.txt",
        success_url="/password_reset/done/"
       ), 
       name="password_reset"),

  path("password_reset/done/", 
       auth_views.PasswordResetDoneView.as_view(
         template_name="registration/password_reset_done.html"
       ), 
       name="password_reset_done"),

  path("reset/<uidb64>/<token>/", 
       auth_views.PasswordResetConfirmView.as_view(
         template_name="registration/password_reset_confirm.html"
       ), 
       name="password_reset_confirm"),

  path("reset/done/", 
       auth_views.PasswordResetCompleteView.as_view(
         template_name="registration/password_reset_complete.html"
       ), 
       name="password_reset_complete"),



    path(
      'login/',
      never_cache(
        ensure_csrf_cookie(
          auth_views.LoginView.as_view(
            template_name='registration/login.html'
          )
        )
      ),
      name='login'
    ),


    path('logout/', app_views.logout_view, name='logout'),


    path('', include('university_marketplace.app1.urls')),
    path("api/", include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
