from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('add-lawyer/', views.add_lawyer, name='add-lawyer'),
    path('lawyer-list/', views.lawyer_list, name='lawyer-list'),  # Assuming you have a lawyer list view


]



