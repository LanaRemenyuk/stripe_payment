from django.urls import path
from .views import BuyItemView, ItemDetailView

urlpatterns = [
    path('buy/<int:id>/', BuyItemView.as_view(), name='buy-item'),
    path('item/<int:id>/', ItemDetailView.as_view(), name='item-detail'),
]
