from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from datetime import timedelta
from dronerental.rentalservice.models import UAV, RentalTransaction, Brand, Category
from django.core.exceptions import ValidationError


class RentalTransactionAvailabilityTest(TestCase):
    def setUp(self):
        # Test için bir UAV örneği oluştur
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass123')
        self.brand = Brand.objects.create(name="DJI",
                                          description="Leading in civilian drones and aerial imaging technology.")
        self.category = Category.objects.create(name="Aerial Photography",
                                                description="UAVs designed for aerial photography and videography.")
        self.uav = UAV.objects.create(
            name='Test UAV',
            description='Test description',
            hourly_rate=100,
            max_payload=5.0,
            range=500,
            endurance=120,
            weight=2.0,
            operating_conditions='Optimal',
            camera_quality='4K',
            night_flight_capable=True,
            brand=self.brand,
            category=self.category,
        )

        # Başlangıç ve bitiş tarihleri ile bir RentalTransaction örneği oluştur
        self.start_date = timezone.now()
        self.end_date = self.start_date + timedelta(days=1)
        RentalTransaction.objects.create(
            uav=self.uav,
            user=self.user,
            start_date=self.start_date,
            end_date=self.end_date
        )

    def test_uav_availability(self):
        # Aynı tarihlerde başka bir RentalTransaction oluşturmayı dene
        with self.assertRaises(ValidationError):
            new_transaction = RentalTransaction(
                uav=self.uav,
                start_date=self.start_date,
                end_date=self.end_date
            )
            new_transaction.full_clean()  # Modelin clean metodunu çağırarak validasyon hatasını tetikle
            new_transaction.save()
