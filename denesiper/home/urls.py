from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('add-lawyer/', views.add_lawyer, name='add-lawyer'),
    path('lawyer-list/', views.lawyer_list, name='lawyer-list'),  # Assuming you have a lawyer list view
    path('lawyer/<int:pk>/', views.lawyer_profile, name='lawyer_profile'),
    path('lawyers/', views.lawyer_list, name='lawyer-list'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('contact/', views.contact, name='contact'),
    path('admin/lawyers/', views.admin_lawyer_list, name='admin_lawyer_list'),
    
    path('admin/lawyer/edit/<int:pk>/', views.admin_lawyer_edit, name='admin_lawyer_edit'),
    path('admin/lawyer/delete/<int:pk>/', views.admin_lawyer_delete, name='admin_lawyer_delete'),

    path('admin-signin/', views.admin_signin, name='admin_signin'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),


]



