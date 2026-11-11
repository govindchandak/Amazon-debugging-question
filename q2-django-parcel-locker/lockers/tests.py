import json
from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from .models import Locker, Parcel


class ParcelLockerTests(TestCase):
    def post(self, url, body):
        return self.client.post(url, data=json.dumps(body), content_type="application/json")

    def deposit(self, tracking_id, size):
        return self.post("/api/parcels/deposit/", {"tracking_id": tracking_id, "size": size})

    def pickup(self, tracking_id, code):
        return self.post("/api/parcels/pickup/", {"tracking_id": tracking_id, "code": code})

    def make_lockers(self, *sizes):
        for i, size in enumerate(sizes, start=1):
            Locker.objects.create(code=f"{size}{i}", size=size)

    def deposited_ago(self, tracking_id, age):
        Parcel.objects.filter(tracking_id=tracking_id).update(deposited_at=timezone.now() - age)

    # ---------- deposit ----------

    def test_deposit_gives_locker_and_6_digit_code(self):
        self.make_lockers("S", "M", "L")
        response = self.deposit("AMZ1", "S")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["locker"], "S1")
        self.assertEqual(len(response.json()["pickup_code"]), 6)

    def test_medium_parcel_never_goes_in_a_small_locker(self):
        self.make_lockers("S", "L")
        response = self.deposit("AMZ1", "M")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["locker"], "L2")

    def test_small_parcel_uses_medium_locker_when_no_small_is_free(self):
        self.make_lockers("M", "L")
        response = self.deposit("AMZ1", "S")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["locker"], "M1")

    def test_no_free_locker_returns_409(self):
        self.make_lockers("S")
        self.deposit("AMZ1", "S")
        response = self.deposit("AMZ2", "S")
        self.assertEqual(response.status_code, 409)

    def test_same_tracking_id_twice_returns_409(self):
        self.make_lockers("S", "S")
        self.deposit("AMZ1", "S")
        response = self.deposit("AMZ1", "S")
        self.assertEqual(response.status_code, 409)

    # ---------- pickup ----------

    def test_pickup_with_correct_code(self):
        self.make_lockers("S")
        code = self.deposit("AMZ1", "S").json()["pickup_code"]
        response = self.pickup("AMZ1", code)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "PICKED_UP")

    def test_pickup_with_wrong_code_returns_403(self):
        self.make_lockers("S")
        code = self.deposit("AMZ1", "S").json()["pickup_code"]
        wrong = "000000" if code != "000000" else "111111"
        response = self.pickup("AMZ1", wrong)
        self.assertEqual(response.status_code, 403)

    def test_pickup_frees_the_locker(self):
        self.make_lockers("S")
        code = self.deposit("AMZ1", "S").json()["pickup_code"]
        self.pickup("AMZ1", code)
        response = self.client.get("/api/lockers/free/?size=S")
        self.assertEqual(response.json()["free"], 1)

    def test_pickup_on_day_2_is_allowed(self):
        self.make_lockers("S")
        code = self.deposit("AMZ1", "S").json()["pickup_code"]
        self.deposited_ago("AMZ1", timedelta(days=2, hours=23))
        response = self.pickup("AMZ1", code)
        self.assertEqual(response.status_code, 200)

    def test_pickup_after_3_days_returns_410(self):
        self.make_lockers("S")
        code = self.deposit("AMZ1", "S").json()["pickup_code"]
        self.deposited_ago("AMZ1", timedelta(days=3, hours=1))
        response = self.pickup("AMZ1", code)
        self.assertEqual(response.status_code, 410)

    # ---------- free lockers ----------

    def test_free_count_includes_bigger_lockers(self):
        self.make_lockers("S", "M", "L")
        response = self.client.get("/api/lockers/free/?size=M")
        self.assertEqual(response.json()["free"], 2)
