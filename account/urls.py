from django.urls import path
from .views import signup, ajax_reg, signin, signout, profile, users, confirm_user, deactivate_user

urlpatterns = [
    # path('', index),
    path('signup', signup),
    path('signin', signin),
    path('logout', signout),
    path('ajax_reg', ajax_reg),
    path('profile', profile),
    path('users', users),
    path('confirm_user/<int:user_id>', confirm_user),
    path('deactivate_user/<int:user_id>', deactivate_user),
]
