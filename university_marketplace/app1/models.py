from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    university_email = models.EmailField(unique=True)
    favorites        = models.ManyToManyField(
                          "Listing",            # because Listing is in this file
                          blank=True,
                          related_name="favorited_by",
                      )
    photo = models.ImageField(
        upload_to="profile_photos/",
        blank=True,
        null=True,
        help_text="Optional profile picture"
    )
    def __str__(self):
        return self.user.get_full_name() or self.user.username

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Listing(models.Model):
    seller      = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="listings")
    title       = models.CharField(max_length=200)
    description = models.TextField()
    price       = models.DecimalField(max_digits=8, decimal_places=2)
    tags        = models.ManyToManyField(Tag, blank=True, related_name="listings")
    created_at  = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="listings")
    def __str__(self):
        return f"{self.title} — ${self.price}"

class ListingImage(models.Model):
    listing     = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="images")
    image       = models.ImageField(upload_to="listings/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.listing.title} at {self.uploaded_at}"

class Appointment(models.Model):
    listing        = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="appointments")
    buyer          = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="appointments")
    scheduled_time = models.DateTimeField()
    confirmed      = models.BooleanField(default=False)
    completed      = models.BooleanField(default=False)    # NEW

    def __str__(self):
        return f"Appt for {self.listing.title} by {self.buyer}"
class Report(models.Model):
    listing   = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="reports")
    reporter  = models.ForeignKey(Profile, on_delete=models.CASCADE)
    reason    = models.TextField()
    created_at= models.DateTimeField(auto_now_add=True)
class Message(models.Model):
    listing   = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="messages")
    sender    = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="sent_messages")
    recipient = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="received_messages")
    content   = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read   = models.BooleanField(default=False)
    class Meta:
        ordering = ["timestamp"]

    def __str__(self):
        return f"{self.sender} → {self.recipient} @ {self.timestamp}"

class Review(models.Model):
    listing   = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    reviewer  = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE
    )
    rating    = models.PositiveSmallIntegerField(
        choices=[(i, "★" * i) for i in range(1, 6)]
    )
    comment   = models.TextField()
    created   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return f"{self.reviewer} rated {self.listing} {self.rating} stars"
# app1/models.py


