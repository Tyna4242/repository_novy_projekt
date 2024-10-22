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


'''class OrderLineModelTest(TestCase):
    def setUp(self):
        # Vytvoříme instanci produktu a objednávky pro testy
        self.category = Category.objects.create(name="Petr")
        self.product = Product.objects.create(
            title="rohlik",
            category=self.category,
            price=100,
            unit="kilogram",
            stock_quantity=1,
        )
        self.order = Order.objects.create(
            delivery_address="Test",
            user=self.product,
            order_date=date.today(),
            total_cost=200)

    def test_create_order_line(self):
        # Vytvoříme OrderLine a uložíme ho do databáze
        order_line = OrderLine.objects.create(order=self.order, product=self.product, quantity=1, price=200)
        self.order = Order.objects.create(delivery_address="Test Customer")

        # Ověříme, že je order_line uložen správně
        self.assertEqual(order_line.self.order.delivery_address, "Test")
        self.assertEqual(order_line.product, self.product)
        self.assertEqual(order_line.quantity, 1)
        self.assertEqual(order_line.price, 200.00)

    def test_str_method(self):
        # Vytvoříme OrderLine pro testování __str__ metody
        order_line = OrderLine.objects.create(order=self.order, product=self.product, quantity=3, price=300.00)

        # Ověříme, že __str__ metoda vrací očekávaný string
        self.assertEqual(str(order_line), "3 x Test Product at 300.00")

    def test_order_line_default_quantity(self):
        # Vytvoříme OrderLine s výchozí hodnotou quantity
        order_line = OrderLine.objects.create(order=self.order, product=self.product, price=100.00)

        # Ověříme, že quantity je nastaveno na výchozí hodnotu 1
        self.assertEqual(order_line.quantity, 1)


class CommentModelTest(TestCase):
    def setUp(self):
        # Vytvoříme produkt pro přiřazení k komentáři
        self.category = Category.objects.create(name="Petr")
        self.product = Product.objects.create(
            title="rohlik",
            category=self.category,
            price=100,
            unit="kilogram",
            stock_quantity=1,
        )
        self.comment = Comment.objects.create(text="Test Product")

    def test_create_comment(self):
        # Vytvoříme komentář a uložíme ho do databáze
        self.comment = Comment.objects.create(text="Great product!", product=self.product)
        self.product = Product.objects.create(
            title="rohlik",
            category=self.category,
            price=100,
            unit="kilogram",
            stock_quantity=1,
        )
        # Ověříme, že je komentář uložen správně
        self.assertEqual(self.comment.text, "Great product!")
        self.assertEqual(self.product.title, "rohlik")

    def test_comment_max_length(self):
        # Ověříme maximální délku textu komentáře
        comment = Comment.objects.create(text="A" * 129, product=self.product)
        with self.assertRaises(Exception) as context:
            comment.full_clean()  # Ověříme validaci
        self.assertTrue('ensure this value has at most 128 characters' in str(context.exception)) '''