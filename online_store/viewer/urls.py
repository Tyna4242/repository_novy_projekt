from django.urls import path
from .views import MainPageView, BasePageView, PotravinyView, ProductCreateView, ProductUpdateView, ProductDeleteView, IndexView, SignUpView, CategoryView
from .views import PotravinyDetailedView, CommentCreateView, send_email_to_user, api_get_all_products, api_get_all_comments, CategoryDetailView
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [
    path('', MainPageView.as_view(), name='main-view'),
    path('potraviny/', PotravinyView.as_view(), name='potraviny-view'),
    path('category/', CategoryView.as_view(), name='category-view'),
    path('category/<int:pk>', CategoryDetailView.as_view(), name='category-detail-view'),
    path('base/', BasePageView.as_view(), name='base-view'),
    path('potraviny/create/', ProductCreateView.as_view(), name='potraviny-create-view'),
    path('potraviny/update/<int:pk>/', ProductUpdateView.as_view(), name='potraviny-update-view'),
    path('potraviny/delete/<int:pk>/', ProductDeleteView.as_view(), name='potraviny-delete-view'),
    path('index/', IndexView.as_view(), name='index-view'),
    path('users/logout/', LogoutView.as_view(), name='logout'),
    path('users/login/', LoginView.as_view(), name='login'),
    path('users/register/', SignUpView.as_view(), name='registration'),
    path('potraviny/<pk>', PotravinyDetailedView.as_view(), name='potraviny_detail'),
    path('comment/create/<product_pk>', CommentCreateView.as_view(), name='create_comment'),
    path('send_emails_to_user', send_email_to_user),
    path('api/product/get_all', api_get_all_products),
    path('api/comment/get_all', api_get_all_comments),
]