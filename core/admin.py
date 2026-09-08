from django.contrib import admin
from django.utils import timezone
from .models import Advertisement, Blog, Category, Event, Follow, GalleryItem, Notification, Place, Profile, Report, SiteSettings

admin.site.site_header = "Naatilevide Control Room"
admin.site.site_title = "Naatilevide Admin"
admin.site.index_title = "Manage the Kerala Community Platform"

@admin.action(description="Approve selected content")
def approve_items(modeladmin, request, queryset): queryset.update(status="APPROVED", reviewed_at=timezone.now())

@admin.action(description="Reject selected content")
def reject_items(modeladmin, request, queryset): queryset.update(status="REJECTED", reviewed_at=timezone.now())

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display=("user","district","verified"); list_filter=("verified","district"); search_fields=("user__username","user__email","district"); list_editable=("verified",)

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display=("title","author","status","submitted_at","reviewed_at"); list_filter=("status","category"); search_fields=("title","content","author__username"); actions=[approve_items,reject_items]; readonly_fields=("submitted_at","reviewed_at")

@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display=("name","district","author","status","submitted_at"); list_filter=("status","district"); search_fields=("name","location","description","author__username"); actions=[approve_items,reject_items]; readonly_fields=("submitted_at","reviewed_at")

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display=("title","location","event_date","status","author"); list_filter=("status",); search_fields=("title","location","description"); actions=[approve_items,reject_items]; readonly_fields=("submitted_at","reviewed_at")

@admin.register(GalleryItem)
class GalleryAdmin(admin.ModelAdmin):
    list_display=("caption","author","status","submitted_at"); list_filter=("status",); search_fields=("caption","author__username")

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display=("follower","following"); search_fields=("follower__username","following__username")

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin): search_fields=("name",)

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display=("target_type","target_id","reporter","resolved","created_at"); list_filter=("target_type","resolved"); search_fields=("reason","details","reporter__username"); list_editable=("resolved",)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display=("user","text","read","created_at"); list_filter=("read",); search_fields=("user__username","text")

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request): return not SiteSettings.objects.exists()

@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display=("title","shop_name","media_type","enabled","start_at","end_at"); list_filter=("media_type","enabled"); search_fields=("title","shop_name"); list_editable=("enabled",)
