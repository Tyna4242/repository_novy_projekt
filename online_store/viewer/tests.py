# pip install selenium
# tests.py
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from django.contrib.auth.models import User
import time
from django.test import TestCase
from datetime import date
from django.contrib.auth import get_user_model
from .models import OrderLine, Order, Comment, Product, Category, PotravinyFeatures, CustomUser

class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Petr")
        self.product = Product.objects.create(
            title="rohlik",
            category=self.category,
            price=100,
            unit="kilogram",
            stock_quantity=1,
        )

    def test_product_creation(self):
        self.assertEqual(self.product.title, "rohlik")
        self.assertEqual(self.product.price, 100)
        self.assertEqual(self.product.category.name, "Petr")
        self.assertEqual(self.product.unit, "kilogram")
        self.assertEqual(self.product.stock_quantity, 1)


User = get_user_model()


class MySeleniumTests(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Set up the WebDriver (make sure the path is correct if needed)
        cls.selenium = webdriver.Chrome()
        cls.selenium.implicitly_wait(10)

        cls.admin_user = User.objects.create_superuser(
            username='admin',
            password='admin',
            email='admin@example.com'
        )

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        # Access the live server URL
        self.selenium.get(f'{self.live_server_url}/users/login/')
        time.sleep(2)
        # Find the username and password input fields and fill them
        username_input = self.selenium.find_element(By.NAME, "username")
        password_input = self.selenium.find_element(By.NAME, "password")
        username_input.send_keys('admin')
        password_input.send_keys('admin')
        time.sleep(2)
        # Submit the form
        self.selenium.find_element(By.XPATH, '//input[@type="submit"]').click()
        time.sleep(2)

        # Test that we successfully logged in (check for a successful redirect or message)
        self.assertIn("Logout - admin", self.selenium.page_source)



from viewer.models import OrderLine, Order, Product, CustomUser, Category

class OrderLineModelTest(TestCase):
    def setUp(self):
        # Create a user, category, and product
        self.user = CustomUser.objects.create_user(username="testuser", password="password")
        category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            title="rohlik",
            description="sobotni",
            thumbnail="image.jpg",
            category=category,
            price=4,
            stock_quantity=5,
            unit="kg"
        )
        self.order = Order.objects.create(
            user=self.user,
            delivery_address="hlavni",
            status="pending"
        )
    
    def test_create_order_line(self):
        # Create an order line for the product and order
        order_line = OrderLine.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            price=self.product.price
        )
        
        # Check that the order line was created and associated with the correct order and product
        self.assertEqual(order_line.order, self.order)
        self.assertEqual(order_line.product, self.product)
        self.assertEqual(order_line.quantity, 2)
        self.assertEqual(OrderLine.objects.count(), 1)


from viewer.models import Comment, Product, Category

class CommentModelTest(TestCase):
    def setUp(self):
        # Create a category and product
        category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            title="rohlik",
            description="sobotni",
            thumbnail="image.jpg",
            category=category,
            price=999.99,
            stock_quantity=10,
            unit="kg"
        )
    
    def test_create_comment(self):
        # Create a comment for the product
        comment = Comment.objects.create(
            text="Great product!",
            product=self.product
        )
        
        # Check that the comment was created and associated with the correct product
        self.assertEqual(comment.text, "Great product!")
        self.assertEqual(comment.product, self.product)
        self.assertEqual(Comment.objects.count(), 1)
