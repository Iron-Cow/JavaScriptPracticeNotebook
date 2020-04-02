from django.urls import path
from .views import index, problems_list, add_language, js_editor

urlpatterns = [
    path('', index),
    path('problems_list', problems_list),
    path('add_language', add_language),
    path('js_editor', js_editor),
]