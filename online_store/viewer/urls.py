from django.urls import path
from .views import MainPageView, BasePageView, PotravinyView, ProductCreateView, ProductUpdateView, ProductDeleteView, IndexView, SignUpView, CategoryView, ProfileView
from .views import PotravinyDetailedView, CommentCreateView, send_email_to_user, api_get_all_products, api_get_all_comments, CategoryDetailView, update_profile, OrderHistoryView, update_category_order, Index2View
from django.contrib.auth.views import LogoutView, LoginView
from .views import add_to_cart, cart_view, place_order, ThankYouPageView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', MainPageView.as_view(), name='main-view'),
    path('category/', CategoryView.as_view(), name='category-view'),
    path('category/<int:pk>', CategoryDetailView.as_view(), name='category-detail-view'),
    path('base/', BasePageView.as_view(), name='base-view'),
    path('potraviny/create/', ProductCreateView.as_view(), name='potraviny-create-view'),
    path('potraviny/update/<int:pk>/', ProductUpdateView.as_view(), name='potraviny-update-view'),
    path('potraviny/delete/<int:pk>/', ProductDeleteView.as_view(), name='potraviny-delete-view'),
    path('index/', IndexView.as_view(), name='index-view'),
    path('index2/', Index2View.as_view(), name='index-2-view'),
    path('users/logout/', LogoutView.as_view(), name='logout'),
    path('users/login/', LoginView.as_view(), name='login'),
    path('users/register/', SignUpView.as_view(), name='registration'),
    path('potraviny/<pk>', PotravinyDetailedView.as_view(), name='potraviny_detail'),
    path('comment/create/<product_pk>', CommentCreateView.as_view(), name='create_comment'),
    path('send_emails_to_user', send_email_to_user),
    path('api/product/get_all', api_get_all_products),
    path('api/comment/get_all', api_get_all_comments),
    path('cart/add/<int:product_id>/', add_to_cart, name='add-to-cart'),
    path('cart/', cart_view, name='cart-view'),
    path('cart/order/', place_order, name='place-order'),
    path('thank-you/', ThankYouPageView.as_view(), name='thank_you'),
    path('profil/', ProfileView.as_view(), name='profile'),
    path('update-profil/', update_profile, name='update-profile'),
    path('place-order/', place_order, name='place_order'),
    path('order-history/', OrderHistoryView.as_view(), name='order_history'),
    path('update-category-order/', update_category_order, name='update_category_order'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),