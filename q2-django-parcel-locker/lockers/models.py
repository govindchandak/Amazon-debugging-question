from django.db import models

SIZES = [("S", "Small"), ("M", "Medium"), ("L", "Large")]


class Locker(models.Model):
    code = models.CharField(max_length=10, unique=True)
    size = models.CharField(max_length=1, choices=SIZES)
    is_free = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code} ({self.size})"


class Parcel(models.Model):
    IN_LOCKER = "IN_LOCKER"
    PICKED_UP = "PICKED_UP"

    tracking_id = models.CharField(max_length=30, unique=True)
    size = models.CharField(max_length=1, choices=SIZES)
    locker = models.ForeignKey(Locker, null=True, on_delete=models.SET_NULL)
    pickup_code = models.CharField(max_length=6)
    status = models.CharField(max_length=20, default=IN_LOCKER)
    deposited_at = models.DateTimeField(auto_now_add=True)
