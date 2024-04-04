# your_app/urls.py

from django.urls import path
from .views import RentalTransactionListCreate, RentalTransactionDetail

urlpatterns = [
    path('rentals/', RentalTransactionListCreate.as_view(), name='rental-transactions'),
    path('rentals/<int:pk>/', RentalTransactionDetail.as_view(), name='rental-detail'),
]
