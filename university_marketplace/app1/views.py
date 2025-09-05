# university_marketplace/app1/views.py

from django.shortcuts               import render, redirect, get_object_or_404
from django.http                    import HttpResponse, JsonResponse
from django.conf                    import settings
from django.contrib.auth            import login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache  import never_cache
from django.views.decorators.csrf   import ensure_csrf_cookie
from django.views.decorators.http   import require_POST
from django.contrib                 import messages
from django.db.models               import Q
import requests
from django.contrib.admin.views.decorators import staff_member_required
from .models import Report
from django.shortcuts               import render, redirect
from .forms                         import ProfileForm


from .models import (
    Listing,
    ListingImage,
    Tag,
    Message,
    Profile,
    Appointment,
    Category,
    Report,
    Review,
)
from .forms import (
    SignUpForm,
    ListingForm,
    AppointmentForm,
    ReportForm,
    MessageForm,
    ReviewForm,
    AddImagesForm,
)

@never_cache
@ensure_csrf_cookie
def home(request):
    q   = request.GET.get("q", "")
    tag = request.GET.get("tag", "")
    cat_slug  = request.GET.get("category", "")

    listings = (
        Listing.objects
               .select_related("seller__user","category")
               .prefetch_related("images", "tags")
               .order_by("-created_at")
    )
    if q:
        listings = listings.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q)
        )
    if tag:
        listings = listings.filter(tags__id=tag)
    if cat_slug:
        listings = listings.filter(category__slug=cat_slug)
    all_tags = Tag.objects.all()
    return render(request, "app1/home.html", {
        "listings":    listings,
        "all_tags":    all_tags,
        "all_cats":    Category.objects.all(),
        "current_q":   q,
        "current_tag": tag,
        "current_cat": cat_slug,
    })


def about(request):
    return render(request, "app1/about.html")

def server_info(request):
    server_geodata = requests.get("https://ipwhois.app/json/").json()
    settings_dump  = settings.__dict__
    return HttpResponse(f"{server_geodata}<br><pre>{settings_dump}</pre>")



def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # create the Profile
            profile, created = Profile.objects.get_or_create(user=user)
            profile.university_email = form.cleaned_data["university_email"]

            profile.save()
            login(request, user)
            return redirect("home")
    else:
        form = SignUpForm()
    return render(request, "app1/signup.html", {"form": form})


@login_required
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.seller = request.user.profile
            listing.save()
            form.save_m2m()
            for img in request.FILES.getlist("images"):
                ListingImage.objects.create(listing=listing, image=img)
            
            tags_csv = form.cleaned_data["tags_str"]
            if tags_csv:
                for name in tags_csv.split(","):
                    name = name.strip()
                    if not name:
                        continue
                    tag, _ = Tag.objects.get_or_create(name__iexact=name, defaults={"name": name})
                    listing.tags.add(tag)
            return redirect("home")
    else:
        form = ListingForm()
    return render(request, "app1/upload.html", {"form": form})

@never_cache
@ensure_csrf_cookie
def detail_listing(request, pk):
    listing = get_object_or_404(
        Listing.objects
               .select_related("seller__user")
               .prefetch_related("images", "tags"),
        pk=pk
    )

    # ——— AJAX fragments for modals ———
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        frag = request.GET.get("fragment")
        ctx  = {"listing": listing}

        if frag == "description":
            return render(request, "app1/partials/description.html", ctx)

        if frag == "appointment":
            if request.method == "POST":
                form = AppointmentForm(request.POST)
                if form.is_valid():
                    appt = form.save(commit=False)
                    appt.listing = listing
                    appt.buyer   = request.user.profile
                    appt.save()
                    return render(
                        request,
                        "app1/partials/appointment_success.html",
                        {"appt": appt}
                    )
            else:
                form = AppointmentForm()
            ctx["form"] = form
            return render(request, "app1/partials/appointment.html", ctx)

        if frag == "reviews":
            if request.method == "POST":
                form = ReviewForm(request.POST)
                if form.is_valid():
                    rev = form.save(commit=False)
                    rev.listing  = listing
                    rev.reviewer = request.user.profile
                    rev.save()
            else:
                form = ReviewForm()
            ctx.update({
                "form":    form,
                "reviews": listing.reviews.select_related("reviewer__user").all()
            })
            return render(request, "app1/partials/reviews.html", ctx)

        if frag == "report":
            if request.method == "POST":
                form = ReportForm(request.POST)
                if form.is_valid():
                    rpt = form.save(commit=False)
                    rpt.listing  = listing
                    rpt.reporter = request.user.profile
                    rpt.save()
            else:
                form = ReportForm()
            ctx["form"] = form
            return render(request, "app1/partials/report_form.html", ctx)


        return render(request, "app1/partials/description.html", ctx)

    
    form = MessageForm()
    me   = request.user.profile if request.user.is_authenticated else None

    # mark unread as read
    if me:
        Message.objects.filter(
            listing=listing, recipient=me, is_read=False
        ).update(is_read=True)

    # grab thread
    thread = []
    if me:
        thread = (
            Message.objects
                   .filter(listing=listing)
                   .filter(Q(sender=me)|Q(recipient=me))
                   .select_related("sender__user","recipient__user")
                   .order_by("timestamp")
        )

    return render(request, "app1/detail.html", {
        "listing": listing,
        "thread":  thread,
        "form":     form,
    })



from .models import Listing, Message
from .forms  import MessageForm

# app1/views.py
from django.shortcuts       import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache  import never_cache
from django.views.decorators.csrf   import ensure_csrf_cookie
from django.db.models       import Q
from .models                import Listing, Message, Profile
from .forms                 import MessageForm

# app1/views.py

@login_required
@never_cache
@ensure_csrf_cookie
def chat_fragment(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    me      = request.user.profile


    if me != listing.seller:

        buyer = listing.seller

    else:

        participants = (
            Profile.objects
                   .filter(
                     Q(sent_messages__listing=listing) |
                     Q(received_messages__listing=listing)
                   )
                   .exclude(pk=me.pk)      
                   .distinct()
        )


        buyer_id = request.GET.get("buyer") or request.POST.get("buyer")
        if not buyer_id:
            if participants.count() > 1:

                return render(request, "app1/partials/chat_select.html", {
                    "listing":      listing,
                    "participants": participants,
                })
            elif participants.count() == 1:
                buyer = participants.first()
            else:

                return render(request, "app1/partials/chat_select.html", {
                    "listing":      listing,
                    "participants": participants,
                })
        else:
            buyer = get_object_or_404(Profile, pk=buyer_id)


    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.listing   = listing
            msg.sender    = me
            msg.recipient = buyer
            msg.save()
            form = MessageForm()
    else:
        form = MessageForm()


    Message.objects.filter(
        listing=listing,
        sender=buyer,
        recipient=me,
        is_read=False
    ).update(is_read=True)


    thread = Message.objects.filter(listing=listing).filter(
        Q(sender=me,      recipient=buyer) |
        Q(sender=buyer,   recipient=me)
    ).order_by("timestamp")

    return render(request, "app1/partials/chat.html", {
        "listing":      listing,
        "thread":       thread,
        "form":         form,
        "reply_target": buyer,
        "buyer":        buyer,
    })


@login_required
def create_appointment(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appt = form.save(commit=False)
            appt.listing = listing
            appt.buyer   = request.user.profile
            appt.save()
            messages.success(
                request,
                f"📅 Appointment scheduled for {appt.scheduled_time:%b %-d at %I:%M %p}."
            )
            return redirect("detail", pk=pk)
    else:
        form = AppointmentForm()
    return render(request, "app1/appointment_form.html", {
        "form":    form,
        "listing": listing,
    })


@login_required
def listing_reviews(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            rev = form.save(commit=False)
            rev.listing  = listing
            rev.reviewer = request.user.profile
            rev.save()
            messages.success(request, "Thanks for your review!")
            return redirect("listing_reviews", pk=pk)
    else:
        form = ReviewForm()
    reviews = listing.reviews.select_related("reviewer__user").all()
    return render(request, "app1/reviews.html", {
        "listing": listing,
        "form":    form,
        "reviews": reviews,
    })


@login_required
def report_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    if request.method == "POST":
        form = ReportForm(request.POST)
        if form.is_valid():
            rpt = form.save(commit=False)
            rpt.listing  = listing
            rpt.reporter = request.user.profile
            rpt.save()
            messages.success(request, "Listing reported.")
            return redirect("detail", pk=pk)
    else:
        form = ReportForm()
    return render(request, "app1/report_form.html", {
        "form":    form,
        "listing": listing,
    })


@login_required
def delete_listing(request, pk):
    if request.user.is_staff:
        listing=get_object_or_404(Listing, pk=pk)
    else:
        listing = get_object_or_404(Listing, pk=pk, seller=request.user.profile)
    if request.method == "POST":
        listing.delete()
        return redirect("home")
    return render(request, "app1/confirm_delete.html", {"listing": listing})


@login_required
@require_POST
def mark_read(request):
    Message.objects.filter(
        recipient=request.user.profile,
        is_read=False
    ).update(is_read=True)
    return HttpResponse(status=204)


@login_required
@require_POST
def complete_appointment(request, pk):
    appt = get_object_or_404(
        Appointment,
        pk=pk,
        listing__seller=request.user.profile,
        completed=False
    )
    appt.completed = True
    appt.save()
    return redirect(request.META.get("HTTP_REFERER", "home"))


@login_required
def get_unread_count(request):
    cnt = Message.objects.filter(recipient=request.user.profile, is_read=False).count()
    return JsonResponse({"unread_count": cnt})


@login_required
def logout_view(request):
    logout(request)
    resp = redirect("home")
    resp.delete_cookie(settings.CSRF_COOKIE_NAME)
    resp.delete_cookie(settings.SESSION_COOKIE_NAME)
    return resp

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

@login_required
def toggle_favorite(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    profile = request.user.profile
    if listing in profile.favorites.all():
        profile.favorites.remove(listing)
        action = "removed"
    else:
        profile.favorites.add(listing)
        action = "added"
    return JsonResponse({"status": "ok", "action": action})
@login_required
def my_wishlist(request):
    favs = request.user.profile.favorites.all()
    return render(request, "app1/wishlist.html", {"favorites": favs})

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q

# at the bottom of app1/views.py

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q

@login_required
def my_recommendations(request):
    profile = request.user.profile
    # get all tag‐ids from their favorites
    tag_ids = profile.favorites.values_list("tags__id", flat=True)
    # find other listings sharing those tags (exclude ones they've already favorited)
    recs = (
        Listing.objects
               .filter(tags__in=tag_ids)
               .exclude(favorited_by=profile)
               .annotate(match_count=Count("tags",
                                          filter=Q(tags__in=tag_ids)))
               .order_by("-match_count","-created_at")[:10]
    )
    return render(request, "app1/recommendations.html", {
        "recommendations": recs,
    })
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Listing

@login_required
def my_listings(request):
    """Show only “view” buttons for everything this user has posted."""
    listings = (
        request.user.profile.listings
               .prefetch_related("images")
               .order_by("-created_at")
    )
    return render(request, "app1/my_listings.html", {
        "listings": listings,
    })

@login_required
def manage_listings(request):
    """Show “remove” buttons so the user can delete any of their own listings."""
    listings = (
        request.user.profile.listings
               .prefetch_related("images")
               .order_by("-created_at")
    )
    return render(request, "app1/manage_listings.html", {
        "listings": listings,
    })
@staff_member_required
@ensure_csrf_cookie
def reported_listings(request):
    """
    Show all user‐submitted reports and let staff delete the offending listing.
    """
    reports = (
        Report.objects
              .select_related("listing__seller__user", "reporter__user")
              .order_by("-created_at")
    )
    return render(request, "app1/reported_listings.html", {
        "reports": reports,
    })
from .models import Listing, ListingImage

@login_required
def add_images(request, pk):
    # only the seller can add to their own listing
    listing = get_object_or_404(Listing, pk=pk, seller=request.user.profile)

    if request.method == "POST":
        # pull *all* the uploaded files from the field named "images"
        files = request.FILES.getlist("images")
        if not files:
            messages.error(request, "Please select at least one image to upload.")
        else:
            for f in files:
                ListingImage.objects.create(listing=listing, image=f)
            messages.success(request, "Your additional images have been added!")
            return redirect("detail", pk=pk)

    return render(request, "app1/add_images.html", {
        "listing": listing,
    })


@login_required
def profile_edit(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_edit')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'app1/profile.html', {
        'form':   form,
        'profile': profile,
    })

def healthz(request):
    return HttpResponse("OK")