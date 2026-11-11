import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from .models import Product, WishlistItem


@require_GET
def list_products(request):
    products = [{"id": p.id, "name": p.name, "price": p.price} for p in Product.objects.order_by("id")]
    return JsonResponse({"products": products})


@csrf_exempt
@require_POST
def add_to_wishlist(request, customer):
    data = json.loads(request.body or "{}")
    product = Product.objects.filter(id=data.get("product_id")).first()
    if product is None:
        return JsonResponse({"error": "Product not found"}, status=404)

    already_saved = WishlistItem.objects.filter(product=product).exists()
    if already_saved:
        return JsonResponse({"error": "Already in wishlist"}, status=409)

    item = WishlistItem(customer=customer, product=product)
    return JsonResponse({"customer": customer, "product": product.name}, status=201)


def _items_for(customer):
    return WishlistItem.objects.filter(customer=customer).select_related("product").order_by("added_at")


@require_GET
def get_wishlist(request, customer):
    items = _items_for(customer)
    return JsonResponse({
        "customer": customer,
        "items": [{"product": i.product.name, "price": i.product.price} for i in items],
        "total": sum(i.product.price for i in items),
    })


@require_GET
def wishlist_page(request, customer):
    items = _items_for(customer)
    context = {
        "customer": customer,
        "wishlist_items": items,
        "total": sum(i.product.price for i in items),
    }
    return render(request, "wishlist/page.html", context)
