from django.test import TestCase
from dronerental.rentalservice.models import Category


class CategoryModelTest(TestCase):

    def setUp(self):
        # Setup run before every test method to create a new category
        self.category = Category.objects.create(name="Surveillance",
                                                description="UAVs equipped for surveillance and monitoring.")

    def test_category_creation(self):
        """Test the category model can create a category."""
        self.assertEqual(self.category.name, "Surveillance")
        self.assertEqual(self.category.description, "UAVs equipped for surveillance and monitoring.")

    def test_category_update(self):
        """Test the category model can update a category."""
        self.category.name = "Aerial Photography"
        self.category.description = "UAVs designed for aerial photography and videography."
        self.category.save()

        updated_category = Category.objects.get(id=self.category.id)
        self.assertEqual(updated_category.name, "Aerial Photography")
        self.assertEqual(updated_category.description, "UAVs designed for aerial photography and videography.")

    def test_category_delete(self):
        """Test the category model can delete a category."""
        category_id = self.category.id
        self.category.delete()
        self.assertFalse(Category.objects.filter(id=category_id).exists())

    def test_category_list(self):
        """Test the category model can list categories."""
        Category.objects.create(name="Delivery", description="UAVs for delivering packages.")
        categories = Category.objects.all()
        self.assertEqual(categories.count(), 2)
        self.assertTrue(categories.filter(name="Surveillance").exists())
        self.assertTrue(categories.filter(name="Delivery").exists())
