from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("profile/<str:username>/", views.profile, name="profile"),
    path("follow/<str:username>/", views.follow, name="follow"),
    path("blog/create/", views.create_blog, name="create_blog"),
    path("place/create/", views.create_place, name="create_place"),
    path("event/create/", views.create_event, name="create_event"),
    path("blog/<int:pk>/", views.blog_detail, name="blog_detail"),
    path("place/<int:pk>/", views.place_detail, name="place_detail"),
    path("report/<str:target_type>/<int:target_id>/", views.report, name="report"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
