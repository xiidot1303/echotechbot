from django.urls import path, re_path
from django.contrib.auth.views import (
    LoginView, 
    LogoutView, 
    PasswordChangeDoneView, 
    PasswordChangeView
)

from app.views import (
    main, promocode
)

urlpatterns = [
    # login
    path('accounts/login/', LoginView.as_view()),
    path('changepassword/', PasswordChangeView.as_view(
        template_name = 'registration/change_password.html'), name='editpassword'),
    path('changepassword/done/', PasswordChangeDoneView.as_view(
        template_name = 'registration/afterchanging.html'), name='password_change_done'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # promocode
    path('generate-promo-codes/', promocode.generate_promo_codes_view, name='generate_promo_codes'),
    path('export-promo-codes/', promocode.export_promo_codes_view, name='export_promo_codes'),

    # files
    re_path(r'^files/(?P<path>.*)$', main.get_file),


]
