from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    photo = models.ImageField(upload_to="profiles/", blank=True, null=True)
    bio = models.TextField(blank=True)
    district = models.CharField(max_length=60, blank=True)
    verified = models.BooleanField(default=False, help_text="Admin controlled. Turn on only after verification.")
    def __str__(self): return self.user.username

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    class Meta:
        constraints = [models.UniqueConstraint(fields=["follower", "following"], name="unique_user_follow")]
    def __str__(self): return f"{self.follower} → {self.following}"

class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    def __str__(self): return self.name

class Moderated(models.Model):
    STATUS = [("PENDING", "Pending verification"), ("APPROVED", "Approved"), ("REJECTED", "Rejected")]
    status = models.CharField(max_length=10, choices=STATUS, default="PENDING")
    rejection_reason = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(blank=True, null=True)
    class Meta: abstract = True

class Blog(Moderated):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blogs")
    title = models.CharField(max_length=180); content = models.TextField()
    cover = models.ImageField(upload_to="blogs/", blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    class Meta: ordering = ["-submitted_at"]
    def __str__(self): return self.title

class Place(Moderated):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="places")
    name = models.CharField(max_length=160); district = models.CharField(max_length=60); location = models.CharField(max_length=220)
    description = models.TextField(); image = models.ImageField(upload_to="places/", blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    class Meta: ordering = ["-submitted_at"]
    def __str__(self): return self.name

class Event(Moderated):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")
    title = models.CharField(max_length=180); location = models.CharField(max_length=220); event_date = models.DateTimeField()
    description = models.TextField(); image = models.ImageField(upload_to="events/", blank=True, null=True)
    class Meta: ordering = ["event_date"]
    def __str__(self): return self.title

class GalleryItem(Moderated):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="gallery")
    image = models.ImageField(upload_to="gallery/"); caption = models.CharField(max_length=220, blank=True)
    def __str__(self): return self.caption or f"Gallery #{self.pk}"

class Report(models.Model):
    TARGETS = [("BLOG", "Blog"), ("PLACE", "Place"), ("EVENT", "Event"), ("USER", "User")]
    target_type = models.CharField(max_length=10, choices=TARGETS); target_id = models.PositiveIntegerField()
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reports")
    reason = models.CharField(max_length=180); details = models.TextField(blank=True); resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ["-created_at"]
    def __str__(self): return f"{self.target_type} #{self.target_id}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    text = models.CharField(max_length=255); read = models.BooleanField(default=False); created_at = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ["-created_at"]
    def __str__(self): return self.text[:60]

class SiteSettings(models.Model):
    hero_title = models.CharField(max_length=180, default="Naatilevide")
    hero_text = models.TextField(default="Naattinte kathakal, sthalangal, aalkkaar — ellam oru idath.")
    hero_image = models.ImageField(upload_to="site/", blank=True, null=True)
    about_title = models.CharField(max_length=180, default="Our Kerala"); about_text = models.TextField(blank=True)
    favicon = models.ImageField(upload_to="site/", blank=True, null=True); adsense_enabled = models.BooleanField(default=False)
    adsense_client = models.CharField(max_length=120, blank=True)
    def __str__(self): return "Naatilevide Site Settings"

class Advertisement(models.Model):
    MEDIA_TYPES = [("IMAGE", "Image"), ("VIDEO", "Video")]
    title = models.CharField(max_length=180); shop_name = models.CharField(max_length=160)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES, default="IMAGE")
    image = models.ImageField(upload_to="ads/images/", blank=True, null=True); video = models.FileField(upload_to="ads/videos/", blank=True, null=True)
    target_url = models.URLField(blank=True); enabled = models.BooleanField(default=False)
    start_at = models.DateTimeField(blank=True, null=True); end_at = models.DateTimeField(blank=True, null=True); created_at = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ["-created_at"]
    def is_live(self):
        now = timezone.now()
        return self.enabled and (self.start_at is None or self.start_at <= now) and (self.end_at is None or self.end_at >= now)
    def __str__(self): return f"{self.shop_name} — {self.title}"
