from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('',views.index, name='index'),
    path('home',views.home, name='home'),
    path('details/<int:pk>',views.details, name='details'),
    path('form',views.create_data, name='form'),
    path('profile',views.profile, name='profile'),
    path('edit_profile',views.edit_profile, name='edit_profile'),
    path('contact',views.contact,name='contact'),
    path('signup',views.signup,name='signup'),
    path('login',views.login_view, name='login'),
    path('logout',views.logout_view, name='logout'),
    path('validate_code/', views.validate_code, name='validate_code'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
