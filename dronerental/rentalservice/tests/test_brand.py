from django.test import TestCase
from dronerental.rentalservice.models import Brand

class BrandModelTest(TestCase):

    def setUp(self):
        # Setup run before every test method.
        Brand.objects.create(name="DJI", description="Leading brand in civilian drones and aerial imaging technology.")

    def test_brand_creation(self):
        """Test the brand model can create a brand."""
        brand = Brand.objects.get(name="DJI")
        self.assertEqual(brand.name, "DJI")
        self.assertEqual(brand.description, "Leading brand in civilian drones and aerial imaging technology.")

    def test_brand_update(self):
        """Test the brand model can update a brand."""
        brand = Brand.objects.get(name="DJI")
        brand.name = "DJI Updated"
        brand.save()
        self.assertEqual(Brand.objects.get(id=brand.id).name, "DJI Updated")

    def test_brand_delete(self):
        """Test the brand model can delete a brand."""
        brand = Brand.objects.get(name="DJI")
        brand_id = brand.id
        brand.delete()
        self.assertFalse(Brand.objects.filter(id=brand_id).exists())

    def test_brand_list(self):
        """Test the brand model can list brands."""
        Brand.objects.create(name="Parrot", description="Innovative and high performance drones.")
        brands = Brand.objects.all()
        self.assertEqual(brands.count(), 2)
        self.assertTrue(brands.filter(name="DJI").exists())
        self.assertTrue(brands.filter(name="Parrot").exists())
