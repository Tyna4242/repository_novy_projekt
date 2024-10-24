

# Create your views here.
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, FormView, ListView, DetailView
from .models import Category, Product, Comment, Order, OrderLine, PromoCode
from django.urls import reverse_lazy
from viewer.forms import ProductForm, CommentForm, CustomUserCreationForm, CustomUserUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
import requests
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Order 
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.models import Q
from django.views.generic import DetailView
from .models import CustomUser



# ZÁKLADNÍ TEMPLATES

class MainPageView(TemplateView):
    template_name = "viewer/main.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch weather info if user is logged in
        if self.request.user.is_authenticated:
            user_city = self.request.user.city
            if user_city:
                # Fetch weather data from OpenWeatherMap API
                api_key = settings.OPENWEATHERMAP_API_KEY
                url = f'http://api.openweathermap.org/data/2.5/weather?q={user_city}&appid={api_key}&units=metric'

                response = requests.get(url)
                if response.status_code == 200:
                    weather_data = response.json()
                    context['weather_info'] = {
                        'city': weather_data['name'],
                        'temperature': weather_data['main']['temp'],
                        'description': weather_data['weather'][0]['description'],
                        'icon': weather_data['weather'][0]['icon'],
                    }
                else:
                    context['weather_info'] = None  # API call failed, no weather info
            else:
                context['weather_info'] = None  # No city defined for the user
        else:
         context['weather_info'] = None  # User not authenticated

        return context

class BasePageView(TemplateView):
    template_name = "base.html"
    extra_context = {}

class PotravinyView(TemplateView):
    template_name = "viewer/potraviny.html"
    extra_context = {
        'all_category': Category.objects.all(),
        'all_product': Product.objects.all()
    }

# KATEGORIE

class CategoryView(ListView):
    model = Category
    template_name = "viewer/category.html"
    context_object_name = 'categories'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        categories = Category.objects.filter(parent__isnull=True).prefetch_related('children')

        query = self.request.GET.get('q')
        if query:
            categories = categories.filter(Q(name__icontains=query) | Q(children__name__icontains=query)).distinct()
        
        paginator = Paginator(categories, 10)  # Počet kategorií na stránku
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context['parent_categories'] = page_obj
        return context


class CategoryDetailView(DetailView):
   model = Category
   template_name = 'viewer/category_detail.html'
   extra_context = {
        'all_category': Category.objects.all(),
        'all_product': Product.objects.all()
    }
   

   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      products = Product.objects.filter(category=self.object)
      
      query = self.request.GET.get('q')
      if query:
         products = products.filter(title__icontains=query)
     
      min_price = self.request.GET.get('min_price')
      max_price = self.request.GET.get('max_price')

      if min_price:
            products = products.filter(price__gte=min_price)
      if max_price:
            products = products.filter(price__lte=max_price)

      paginator = Paginator(products, 10)
      page_number = self.request.GET.get('page')
      page_obj = paginator.get_page(page_number)
      context['products_detail'] = page_obj
      return context

# POTRAVINY 

class PotravinyDetailedView(TemplateView):
  template_name = 'viewer/potraviny_detail.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data( **kwargs)
    context["potraviny_detail"] = Product.objects.get(pk=int(kwargs["pk"]))
    context["potraviny_comments"] = Comment.objects.filter(product__pk=int(kwargs["pk"]))
    return context

class ProductCreateView( LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'viewer/form.html'
    form_class = ProductForm
    model = Product
    success_url = reverse_lazy('category-view')
    permission_required = 'viewer.create_product'

class ProductUpdateView( LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'viewer/form.html'
    form_class = ProductForm
    model = Product
    success_url = reverse_lazy('category-view')
    permission_required = 'viewer.update_product'

class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Product
    template_name = 'viewer/product_confirm_delete.html'
    success_url = reverse_lazy('category-view')
    permission_required = 'viewer.delete_product'
 
# ZKOUŠKY BOOTSTRAP

class IndexView(TemplateView):
    template_name = "index.html"
    extra_context = {}


class Index2View(TemplateView):
    template_name = "index2.html"
    extra_context = {}


# PROFIL

class SignUpView(CreateView):
  template_name = 'viewer/form.html'
  form_class = CustomUserCreationForm
  success_url = reverse_lazy('login')

class ProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'viewer/profile.html'
    context_object_name = 'user_profile'

    def get_object(self):
        return self.request.user 
    
@login_required
def update_profile(request):
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile') 
    else:
        form = CustomUserUpdateForm(instance=request.user)
    return render(request, 'viewer/update_profile.html', {'form': form})


# KOMENTÁŘ

class CommentCreateView(CreateView):
  template_name = 'viewer/form.html'
  form_class = CommentForm
  success_url = reverse_lazy("category-view")

  def form_valid(self, form):
    new_comment : Comment = form.save(commit=False)
    new_comment.product = Product.objects.get(pk=int(self.kwargs["product_pk"]))
    new_comment.save()
    return super().form_valid(form)
  
# OBJEDNÁVKY


def calculate_total_cost(cart):
    total = 0
    for product_id, item in cart.items():
        total += item['quantity'] * float(item['price'])
    return total

def place_order(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        if not cart:
            messages.error(request, "Your cart is empty!")
            return redirect('cart-view')

        user = request.user
        delivery_address = request.POST.get('delivery_address')
        promo_code_input = request.POST.get('promo_code')

        
        promo_code = None
        if promo_code_input:
            try:
                promo_code = PromoCode.objects.get(code=promo_code_input)
                if not promo_code.is_valid():
                    messages.error(request, "Promo code is invalid or expired.")
                    return redirect('cart-view')
            except PromoCode.DoesNotExist:
                messages.error(request, "Promo code does not exist.")
                return redirect('cart-view')

        # Calculate total cost
        total_cost = calculate_total_cost(cart)

        # Apply discount if a valid promo code is used
        if promo_code:
            total_cost = promo_code.apply_discount(total_cost)
            promo_code.times_used += 1
            promo_code.save()

        # Validate address
        if not delivery_address:
            messages.error(request, "You must provide a delivery address.")
            return redirect('cart-view')

        # Create the order
        order = Order.objects.create(
            user=user,
            delivery_address=delivery_address,
            total_cost=total_cost,
            status='pending',
            promo_code=promo_code_input if promo_code else None  # Save the used promo code
        )

        # Create order lines and update stock
        for product_id, item in cart.items():
            product = Product.objects.get(id=product_id)
            quantity = item['quantity']

            if product.stock_quantity < quantity:
                messages.error(request, f"Not enough stock for {product.title}.")
                return redirect('cart-view')

            product.stock_quantity -= quantity
            product.save()

            OrderLine.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price
            )

        # Clear the cart
        request.session['cart'] = {}
        messages.success(request, "Your order has been successfully placed!")
        return redirect('thank_you')


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})

    if str(product_id) not in cart:
        cart[str(product_id)] = {
            'quantity': 1,
            'price': str(product.price),  
        }
    else:
        cart[str(product_id)]['quantity'] += 1

    
    request.session['cart'] = cart

    
    print(f"Cart contents after adding product {product_id}: {cart}")

    return redirect('cart-view')


@login_required
def cart_view(request):
    cart = request.session.get('cart', {})
    products = []
    total_price = 0

    for product_id, item in cart.items():
        product = Product.objects.get(pk=product_id)
        item_total = int(item['quantity']) * float(item['price'])
        total_price += item_total
        products.append({
            'product': product,
            'quantity': item['quantity'],
            'total': item_total
        })

    context = {
        'products': products,
        'total_price': total_price,
    }
    return render(request, 'viewer/cart.html', context)



@login_required
def order_confirmation(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)
    return render(request, 'viewer/order_confirmation.html', {'order': order})



class ThankYouPageView(TemplateView):
    template_name = "viewer/thank_you.html"


class OrderHistoryView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'viewer/order_history.html'
    context_object_name = 'orders'

    def get_queryset(self):
        
        return Order.objects.filter(user=self.request.user).order_by('-order_date')
    


@require_POST
def update_category_order(request):
    category_ids = request.POST.getlist('category_ids[]') 
    for index, category_id in enumerate(category_ids):
        category = Category.objects.get(id=category_id)
        category.order = index  
        category.save()
    return JsonResponse({'success': True})



def send_email_to_user(request):
    print(f"Máme nové zboží {Product.objects.all()} ")

    return HttpResponse("vše OK")

def api_get_all_products(request):
  all_products = Product.objects.all()
  json_all_products = {}
  for product in all_products:
    json_all_products[product.pk] = {
      "název": str(product.title),
      "popis": str(product.description)
    }

  return JsonResponse(json_all_products)


def api_get_all_comments(request):
  json_all_comments = { comment.pk: {"text":str(comment.text)} for comment in Comment.objects.all()}
  return JsonResponse(json_all_comments)

