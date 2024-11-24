from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Authentication
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Dashboard and Care Recipient Management
    path('', views.dashboard, name='dashboard'),
    path('care_recipient/add/', views.add_care_recipient, name='add_care_recipient'),
    path('care_recipient/<int:id>/', views.view_care_recipient, name='view_care_recipient'),
    path('care_recipient/<int:id>/add_data/', views.add_dynamic_data, name='add_dynamic_data'),
]
