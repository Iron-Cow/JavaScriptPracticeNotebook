from django.urls import path
from .views import signup, ajax_reg, signin, signout, profile, users, confirm_user, deactivate_user, \
    delete_feedback_by_user, admin_feedback_list, delete_feedback_totally, ignore_feedback, feedback_answer

urlpatterns = [
    # path('', index),
    path('signup', signup),
    path('signin', signin),
    path('logout', signout),
    path('ajax_reg', ajax_reg),
    path('profile', profile),
    path('users', users),
    path('admin_feedback_list', admin_feedback_list),
    path('confirm_user/<int:user_id>', confirm_user),
    path('deactivate_user/<int:user_id>', deactivate_user),
    path('detete_feedback/<int:feedback_id>', delete_feedback_by_user),
    path('ignore_feedback/<int:feedback_id>', ignore_feedback),
    path('feedback_answer/<int:feedback_id>', feedback_answer),
]
