from django.shortcuts import render, redirect, get_object_or_404
from .forms import LawyerForm
from .models import Lawyer, Review
from .forms import LawyerSearchForm
from django.contrib import messages
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models import Avg
import random
from django.contrib.auth import authenticate, login, logout


def home(request):
    lawyers = Lawyer.objects.all()  # Fetch all lawyers from the database
    return render(request, 'home/index.html', {'lawyers': lawyers})


def add_lawyer(request):
    if request.method == 'POST':
        form = LawyerForm(request.POST, request.FILES)
        if form.is_valid():
            print("Form is valid!")
            form.save()  # שומר את הנתונים
            return redirect('lawyer-list')
        else:
            print("Form errors:", form.errors)  # הדפס שגיאות
    else:
        form = LawyerForm()
    return render(request, 'home/add_lawyer.html', {'form': form})

from django.db.models import Q

def lawyer_list(request):
    form = LawyerSearchForm(request.GET)  # קבלת הנתונים מהטופס
    lawyers = Lawyer.objects.all()  # שליפת כל עורכי הדין

    if form.is_valid():
        # שליפת נתוני הטופס
        name = form.cleaned_data.get('name')
        specialization = form.cleaned_data.get('specialization')
        location = form.cleaned_data.get('location')
        min_rating = form.cleaned_data.get('min_rating')
        max_price = form.cleaned_data.get('max_price')

        # סינון לפי שם
        if name:
            lawyers = lawyers.filter(
                Q(first_name__icontains=name) | Q(last_name__icontains=name)
            )

        # סינון לפי תחום התמחות
        if specialization:
            lawyers = lawyers.filter(specialization__icontains=specialization)

        # סינון לפי מיקום
        if location:
            lawyers = lawyers.filter(location__icontains=location)

        # סינון לפי דירוג מינימלי
        if min_rating is not None:
            lawyers = lawyers.filter(rating__gte=min_rating)

        # סינון לפי מחיר מקסימלי
        if max_price is not None:
            lawyers = lawyers.filter(price_range__lte=max_price)

    # החזרת התוצאה לעמוד
    return render(request, 'home/lawyer_list.html', {'lawyers': lawyers, 'form': form})



def lawyer_profile(request, pk):
    lawyer = get_object_or_404(Lawyer, pk=pk)
    reviews = lawyer.reviews.all()  # Fetch all reviews for the lawyer

    form = ReviewForm()  # Initialize the form here

    if request.method == 'POST':
        if request.user.is_authenticated:  # Ensure the user is logged in
            form = ReviewForm(request.POST)  # Reassign the form with the posted data
            if form.is_valid():
                review = form.save(commit=False)  # Create the review but don't save yet
                review.lawyer = lawyer  # Assign the lawyer for this review
                review.user = request.user  # Assign the current logged-in user as the reviewer
                review.save()  # Save the review to the database

                # Recalculate the average rating for the lawyer
                lawyer.average_rating = lawyer.reviews.aggregate(Avg('rating'))['rating__avg'] or 0.0
                lawyer.save()

                messages.success(request, "Your review has been submitted.")
                
                # Redirect to the lawyer profile page (prevents form resubmission)
                return redirect('lawyer_profile', pk=pk)
        else:
            messages.error(request, "You need to be logged in to submit a review.")

    # Render the profile page with the form
    return render(request, 'home/lawyer_profile.html', {'lawyer': lawyer, 'reviews': reviews, 'form': form})



def aboutus(request):
    context = {
        "title": "About Us",
        "description": (
            "Our Lawyer Recommendation System is designed to connect users "
            "with suitable lawyers based on their needs and legal preferences."
        ),
        "features": [
            "Type of legal matter (e.g., family law, corporate law, criminal defense).",
            "User's geographic location.",
            "Specific lawyer attributes such as experience, reviews, availability, and fee structure.",
        ],
    }
    return render(request, 'home/aboutus.html', context)

def contact(request):
    random_number = random.randint(1000, 9999)  # יצירת מספר רנדומלי
    return render(request, 'home/contact.html', {'random_number': random_number})


# דף ניהול - רשימת עורכי הדין
def admin_lawyer_list(request):
    if not request.user.is_staff:
        return redirect('home')

    lawyers = Lawyer.objects.all()
    return render(request, 'admin_pages/admin_lawyer_list.html', {'lawyers': lawyers})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Lawyer
from .forms import LawyerForm

def admin_lawyer_edit(request, pk):
    lawyer = get_object_or_404(Lawyer, pk=pk)
    if request.method == 'POST':
        form = LawyerForm(request.POST, request.FILES, instance=lawyer)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = LawyerForm(instance=lawyer)
    return render(request, 'admin_pages/admin_lawyer_edit.html', {'form': form, 'lawyer': lawyer})

def admin_lawyer_delete(request, pk):
    lawyer = get_object_or_404(Lawyer, pk=pk)
    if request.method == 'POST':
        lawyer.delete()
        return redirect('admin_dashboard')
    return render(request, 'admin_pages/admin_lawyer_delete.html', {'lawyer': lawyer})



def admin_signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # אימות המשתמש
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('admin_dashboard')  # מעבר לדשבורד
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'home/admin_signin.html')


@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('admin_signin')

    # שליפת כל עורכי הדין
    lawyers = Lawyer.objects.all()
    return render(request, 'home/admin_dashboard.html', {'lawyers': lawyers})