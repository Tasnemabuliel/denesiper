from django.shortcuts import render, redirect, get_object_or_404
from .forms import LawyerForm
from .models import Lawyer, Review
from .forms import LawyerSearchForm
from django.contrib import messages
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models import Avg

def home(request):
    lawyers = Lawyer.objects.all()  # Fetch all lawyers from the database
    return render(request, 'home/index.html', {'lawyers': lawyers})


def add_lawyer(request):
    if request.method == 'POST':
        form = LawyerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lawyer-list')  # Redirect to the lawyer list page after saving
    else:
        form = LawyerForm()
    return render(request, 'home/add_lawyer.html', {'form': form})

from django.db.models import Q

def lawyer_list(request):
    form = LawyerSearchForm(request.GET)
    lawyers = Lawyer.objects.all()

    if form.is_valid():
        name = form.cleaned_data.get('name')
        specialization = form.cleaned_data.get('specialization')
        location = form.cleaned_data.get('location')
        min_rating = form.cleaned_data.get('min_rating')
        max_price = form.cleaned_data.get('max_price')

        # Filtering logic based on form inputs
        if name:
            lawyers = lawyers.filter(
                Q(first_name__icontains=name) | Q(last_name__icontains=name)
            )
        if specialization:
            lawyers = lawyers.filter(specialization__icontains=specialization)
        if location:
            lawyers = lawyers.filter(location__icontains=location)
        if min_rating:
            lawyers = lawyers.filter(rating__gte=min_rating)
        if max_price:
            lawyers = lawyers.filter(price_range__lte=max_price)

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