from django.shortcuts import render, redirect, get_object_or_404
from .forms import LawyerForm
from .models import Lawyer
from .forms import LawyerSearchForm

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

def lawyer_list(request):
    form = LawyerSearchForm(request.GET)
    lawyers = Lawyer.objects.all()

    if form.is_valid():
        name = form.cleaned_data.get('name')
        specialization = form.cleaned_data.get('specialization')
        location = form.cleaned_data.get('location')

        # Filter lawyers based on search input
        if name:
            lawyers = lawyers.filter(first_name__icontains=name) | lawyers.filter(last_name__icontains=name)
        if specialization:
            lawyers = lawyers.filter(specialization__icontains=specialization)
        if location:
            lawyers = lawyers.filter(location__icontains=location)

    return render(request, 'home/lawyer_list.html', {'lawyers': lawyers, 'form': form})
def lawyer_profile(request, pk):
    lawyer = get_object_or_404(Lawyer, pk=pk)
    return render(request, 'home/lawyer_profile.html', {'lawyer': lawyer})