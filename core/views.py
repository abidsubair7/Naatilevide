from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from .forms import BlogForm, EventForm, PlaceForm, ProfileForm, RegisterForm, ReportForm
from .models import Advertisement, Blog, Event, Follow, Place, SiteSettings

def home(request):
    site = SiteSettings.objects.first()
    blogs = Blog.objects.filter(status="APPROVED").select_related("author", "category")[:9]
    places = Place.objects.filter(status="APPROVED").select_related("author")[:9]
    events = Event.objects.filter(status="APPROVED").select_related("author")[:6]
    ads = [ad for ad in Advertisement.objects.all() if ad.is_live()][:6]
    return render(request, "home.html", {"site": site, "blogs": blogs, "places": places, "events": events, "ads": ads})

def register(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Welcome to Naatilevide!")
            return redirect("home")
    else:
        form = RegisterForm()
    return render(request, "form.html", {"form": form, "title": "Join Naatilevide", "subtitle": "Create your Kerala community profile."})

def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(request.GET.get("next", "home"))
        messages.error(request, "Username or password is incorrect.")
    return render(request, "login.html")

@login_required
def logout_view(request):
    logout(request)
    return redirect("home")

def profile(request, username):
    user = get_object_or_404(User, username=username)
    profile_obj = user.profile
    blogs = Blog.objects.filter(author=user, status="APPROVED")[:9]
    places = Place.objects.filter(author=user, status="APPROVED")[:9]
    followers_count = Follow.objects.filter(following=user).count()
    following_count = Follow.objects.filter(follower=user).count()
    is_following = request.user.is_authenticated and Follow.objects.filter(follower=request.user, following=user).exists()
    return render(request, "profile.html", {"profile_user": user, "profile_obj": profile_obj, "blogs": blogs, "places": places, "followers_count": followers_count, "following_count": following_count, "is_following": is_following})

@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == "POST":
        profile.bio = request.POST.get("bio", "")
        profile.district = request.POST.get("district", "")
        if request.FILES.get("photo"):
            profile.photo = request.FILES["photo"]
        profile.save()
        return redirect("profile", username=request.user.username)
    return render(request, "edit_profile.html", {"profile": profile})

@login_required
def follow(request, username):
    target = get_object_or_404(User, username=username)
    if target != request.user:
        Follow.objects.get_or_create(follower=request.user, following=target)
    return redirect("profile", username=target.username)

@login_required
def create_blog(request):
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False); obj.author = request.user; obj.status = "PENDING"; obj.save()
            messages.success(request, "Blog submitted. Admin verification is required before it becomes public.")
            return redirect("profile", request.user.username)
    else: form = BlogForm()
    return render(request, "form.html", {"form": form, "title": "Write a Blog", "subtitle": "Your post will be reviewed by the Naatilevide admin team."})

@login_required
def create_place(request):
    if request.method == "POST":
        form = PlaceForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False); obj.author = request.user; obj.status = "PENDING"; obj.save()
            messages.success(request, "Place submitted for admin verification.")
            return redirect("profile", request.user.username)
    else: form = PlaceForm()
    return render(request, "form.html", {"form": form, "title": "Add a Place", "subtitle": "Fake or incorrect details will not be published without admin approval."})

@login_required
def create_event(request):
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False); obj.author = request.user; obj.status = "PENDING"; obj.save()
            messages.success(request, "Event submitted for admin verification.")
            return redirect("profile", request.user.username)
    else: form = EventForm()
    return render(request, "form.html", {"form": form, "title": "Add an Event", "subtitle": "Event details become public only after admin verification."})

def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk, status="APPROVED")
    return render(request, "detail.html", {"item": blog, "item_type": "Blog"})

def place_detail(request, pk):
    place = get_object_or_404(Place, pk=pk, status="APPROVED")
    return render(request, "detail.html", {"item": place, "item_type": "Place"})

@login_required
def report(request, target_type, target_id):
    allowed = {"BLOG", "PLACE", "EVENT", "USER"}
    if target_type not in allowed: return redirect("home")
    if request.method == "POST":
        form = ReportForm(request.POST)
        if form.is_valid():
            report_obj = form.save(commit=False); report_obj.target_type = target_type; report_obj.target_id = target_id; report_obj.reporter = request.user; report_obj.save()
            messages.success(request, "Report sent to the admin team.")
            return redirect("home")
    else: form = ReportForm()
    return render(request, "form.html", {"form": form, "title": "Report Content", "subtitle": "The admin team will review this report."})
