from django.urls import path
from . import views
from .views import CustomLoginView, RentalTransactionsListAPIView

urlpatterns = [
    path('', views.index, name='index'),  # Route for the index page
    path('login/', CustomLoginView.as_view(), name='login'),  # Route for the login page
    path('signup/', views.signup_view, name='signup'),  # Route for the signup page
    path('dashboard/', views.user_dashboard, name='user_dashboard'),  # Route for the user dashboard
    path('rentals/', views.rental_list, name='rental_list'),  # Route for the rental list page
    path('uavs/', views.list_uavs, name='list_uavs'),  # Route for the list UAVs page
    path('uavs/rent/<int:uav_id>/', views.get_rent_uav, name='rent_uav'),
    # Route for the rental transactions API
    path('api/rentaltransactions/', RentalTransactionsListAPIView.as_view(), name='api_rental_transactions'),
    # Route for the UAVs API
    path('api/uavs/', views.UAVListAPIView.as_view(), name='api_uavs'),
    # Route for the users API
    path('api/uavs/rent/<int:uav_id>/', views.RentUAVView.as_view(), name='api_rent_uav'),
    path('logout/', views.logout_view, name='logout'),

]