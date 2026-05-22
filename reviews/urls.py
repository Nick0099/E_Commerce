from django.urls import path
from . import views

urlpatterns = [
    path('my/',       views.ReviewDetail.as_view(),         name='my_review'),
    path('my/<int:pk>/', views.ReviewDetail.as_view(),      name='review_detail'),
]