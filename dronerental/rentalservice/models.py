from decimal import Decimal

from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Brand(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class UAV(BaseModel):
    name = models.CharField(max_length=100)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2, help_text="Hourly rental rate in USD", default=0.00)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    weight = models.FloatField()
    max_speed = models.FloatField(null=True)
    max_flight_time = models.FloatField(null=True)
    max_range = models.FloatField(null=True)
    max_altitude = models.FloatField(null=True)
    max_wind_speed = models.FloatField(null=True)
    max_ascent_speed = models.FloatField(null=True)
    max_descent_speed = models.FloatField(null=True)
    max_operating_temperature = models.FloatField(null=True)
    max_operating_humidity = models.FloatField(null=True)
    max_operating_wind_speed = models.FloatField(null=True)
    max_operating_rainfall = models.FloatField(null=True)
    availability = models.BooleanField(default=True)
    max_payload = models.FloatField(help_text="Maximum payload capacity in kilograms (kg)", default=0)
    range = models.IntegerField(help_text="Maximum range in kilometers (km)")
    endurance = models.IntegerField(help_text="Maximum flight time in minutes (min)")
    operating_conditions = models.CharField(max_length=200,
                                            help_text="Optimal operating conditions (e.g., weather, time of day)")
    night_flight_capable = models.BooleanField(default=False, help_text="Whether the UAV is capable of flying at night")
    camera_quality = models.CharField(max_length=100, help_text="Camera resolution and features")

    def __str__(self):
        return self.name


class RentalTransaction(models.Model):
    uav = models.ForeignKey(UAV, on_delete=models.CASCADE, related_name='rentals')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rentals')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    total_cost = models.DecimalField(max_digits=6, decimal_places=2, blank=True)

    def save(self, *args, **kwargs):
        duration_hours = (self.end_time - self.start_time).total_seconds() / 3600
        # Float tipindeki duration_hours'ı Decimal tipine çevir
        duration_hours_decimal = Decimal(str(duration_hours))
        # Decimal çarpımını yap
        self.total_cost = duration_hours_decimal * self.uav.hourly_rate
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.uav.name} rented by {self.user.username}"
