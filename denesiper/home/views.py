from django.shortcuts import render, redirect
from .forms import LawyerForm
from .models import Lawyer

def home(request):
    lawyers = Lawyer.objects.all()  # Fetch all lawyers from the database
    return render(request, 'home/index.html', {'lawyers': lawyers})


def add_lawyer(request):
    if request.method == 'POST':
        form = LawyerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Save the lawyer object
            return redirect('lawyer-list')  # Redirect to the lawyer list page after saving
    else:
        form = LawyerForm()
    
    return render(request, 'home/add_lawyer.html', {'form': form})

def lawyer_list(request):
    # Get all the lawyers from the database
    lawyers = Lawyer.objects.all()

    # Render the list of lawyers to the 'index.html' template
    return render(request, 'home/index.html', {'lawyers': lawyers})