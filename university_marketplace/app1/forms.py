from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Listing, Tag, Report, Review, Category
from .models import Review
from decimal import Decimal, InvalidOperation
from django.forms.widgets import ClearableFileInput
from .models import Profile

class ReviewForm(forms.ModelForm):
    class Meta:
        model  = Review
        fields = ["rating", "comment"]
        widgets = {
            "rating":  forms.Select(attrs={"class":"form-select form-select-sm"}),
            "comment": forms.Textarea(attrs={
                           "class":"form-control form-control-sm",
                           "rows":3,
                           "placeholder":"Write your review…"
                        }),
        }

class SignUpForm(UserCreationForm):
    university_email = forms.EmailField(
        required=True,
        help_text="Enter your official university email address."
    )

    class Meta:
        model = User
        fields = ["username", "university_email", "password1", "password2"]

    def clean_university_email(self):
        email = self.cleaned_data["university_email"]
        domain = email.split("@")[-1]
        if domain.lower() not in ("csuchico.edu", "csuchico.com"):  # adjust as needed
            raise forms.ValidationError("Please use your Chico State email address.")
        return email






class ListingForm(forms.ModelForm):
    images = forms.ImageField(
        label="Cover image",
        required=False,
        help_text="Upload one image now, later you can add more images after clicking either on listing or through view my listing -> edit -> add more images"
    )


    price = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'placeholder': 'e.g. 3.00 or $3.00'
        }),
        help_text="You can include a $ or commas (they’ll be stripped)."
    )

    tags_str = forms.CharField(
        label="Please enter any suitable tags (comma-separated)",
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "e.g. calculus, textbook, dorm"}
        )
    )

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label="What category does this listing fall into?",
        required=False,
        empty_label="(No category)",
        widget=forms.Select()
    )

    class Meta:
        model  = Listing
        fields = ['title', 'description', 'price','category', 'tags_str']

    def clean_price(self):
        raw = self.cleaned_data['price']

        cleaned = raw.replace('$', '').replace(',', '').strip()

        try:
            value = Decimal(cleaned)
        except InvalidOperation:
            raise forms.ValidationError("Enter a valid number for the price (e.g. 3.00).")
        if value < 0:
            raise forms.ValidationError("Price must be zero or positive.")
        return value
    from django import forms
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["scheduled_time"]
        widgets = {

            "scheduled_time": forms.DateTimeInput(attrs={"type": "datetime-local"})
        }
from .models import Listing, Tag, Report 

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ["reason"]
        widgets = {
          "reason": forms.Textarea(attrs={"rows":3, "placeholder":"Why are you reporting this listing?"})
        }
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={
                "rows": 3,
                "class": "form-control form-control-sm",
                "placeholder": "Type your message…"
            })
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model  = Review
        fields = ["rating", "comment"]
        widgets = {
          "comment": forms.Textarea(attrs={"rows":3, "class":"form-control"}),
          "rating":  forms.Select(attrs={"class":"form-select"})
        }
from django.forms.widgets import ClearableFileInput

class MultiFileInput(ClearableFileInput):
    allow_multiple_selected = True

class AddImagesForm(forms.Form):
    images = forms.ImageField(
        widget=MultiFileInput(attrs={"multiple": True}),
        help_text="Select any number of additional images",
    )



class ProfileForm(forms.ModelForm):
    class Meta:
        model  = Profile
        fields = ['photo']
