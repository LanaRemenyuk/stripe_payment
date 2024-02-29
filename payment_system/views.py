import os
import json
import stripe
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.http import HttpResponse, JsonResponse
from dotenv import load_dotenv

from .models import Item, Order

load_dotenv()

STRIPE_SECRET_KEY = os.getenv(
    'STRIPE_SECRET_KEY')
STRIPE_SECRET_KEY_P = os.getenv(
    'STRIPE_SECRET_KEY_PRIMARY')


class BuyItemView(View):
    def get(self, request, id):
        try:
            item = get_object_or_404(Item, id=id)
            if item.currency == 'USD':
                stripe.api_key = STRIPE_SECRET_KEY
            elif item.currency == 'INR':
                stripe.api_key = STRIPE_SECRET_KEY_P
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': item.currency,
                        'product_data': {
                            'name': item.name,
                            'description': item.description,
                        },
                        'unit_amount': int(item.price * 100),
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri('/success/'),
                cancel_url=request.build_absolute_uri('/cancel/'),
            )
            return JsonResponse({'session_id': session.id})
        except Exception as e:
            return JsonResponse({'error': str(e)})


class ItemDetailView(View):
    def get(self, request, id):
        try:
            item = Item.objects.get(id=id)
            if item.currency == 'USD':
                stripe_publishable_key = os.getenv('STRIPE_PUBLIC_KEY')
            elif item.currency == 'INR':
                stripe_publishable_key = os.getenv('STRIPE_PUBLIC_KEY_P')
            return render(request, 'item.html', {'item': item, 'stripe_publishable_key': stripe_publishable_key})
        except Item.DoesNotExist:
            return HttpResponse(status=404)