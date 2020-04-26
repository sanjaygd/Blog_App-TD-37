from django.urls import path

from .views import post_list,post_details,post_create,post_update,post_delete

app_name = 'blog_app'
urlpatterns = [
    path('',post_list, name='post_list'),
    # path('details/<int:pk>/',post_details, name='post_details'),
    path('details/<slug:slug>/',post_details, name='post_details'),
    path('create/',post_create, name='post_create'),
    path('update/<int:id>/',post_update, name='post_update'),
    path('delete/<int:id>/',post_delete, name='post_delete')
]
