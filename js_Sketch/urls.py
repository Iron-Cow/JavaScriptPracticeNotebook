from django.urls import path
from .views import index, problems_list, add_language, js_editor, edit_problem, delete_problem, delete_language

urlpatterns = [
    path('', index),
    path('problems_list', problems_list),
    path('add_language', add_language),
    path('delete_language/<int:language_id>', delete_language),
    path('js_editor', js_editor),
    path('problem/<int:problem_id>/edit', edit_problem),
    path('problem/<int:problem_id>/delete', delete_problem),
]