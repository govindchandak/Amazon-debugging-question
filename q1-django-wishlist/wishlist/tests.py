import json

from django.test import TestCase

from .models import Product, WishlistItem


class WishlistTests(TestCase):
    def setUp(self):
        self.kindle = Product.objects.create(name="Kindle", price=9999)
        self.echo = Product.objects.create(name="Echo Dot", price=4499)

    def add(self, customer, product_id):
        return self.client.post(
            f"/api/wishlist/{customer}/items/",
            data=json.dumps({"product_id": product_id}),
            content_type="application/json",
        )

    def test_list_products(self):
        response = self.client.get("/api/products/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["products"]), 2)

    def test_add_unknown_product_returns_404(self):
        response = self.add("alice", 999)
        self.assertEqual(response.status_code, 404)

    def test_added_item_is_saved(self):
        response = self.add("alice", self.kindle.id)
        self.assertEqual(response.status_code, 201)

        wishlist = self.client.get("/api/wishlist/alice/").json()
        self.assertEqual(wishlist["items"], [{"product": "Kindle", "price": 9999}])
        self.assertEqual(wishlist["total"], 9999)

    def test_same_product_twice_returns_409(self):
        WishlistItem.objects.create(customer="alice", product=self.kindle)
        response = self.add("alice", self.kindle.id)
        self.assertEqual(response.status_code, 409)

    def test_two_customers_can_save_the_same_product(self):
        WishlistItem.objects.create(customer="alice", product=self.kindle)
        response = self.add("bob", self.kindle.id)
        self.assertEqual(response.status_code, 201)

    def test_page_shows_saved_items(self):
        WishlistItem.objects.create(customer="alice", product=self.kindle)
        WishlistItem.objects.create(customer="alice", product=self.echo)
        html = self.client.get("/wishlist/alice/").content.decode()
        self.assertIn("Kindle", html)
        self.assertIn("Echo Dot", html)
        self.assertIn("Total: ₹14498", html)

    def test_page_for_empty_wishlist(self):
        html = self.client.get("/wishlist/bob/").content.decode()
        self.assertIn("Your wishlist is empty.", html)
