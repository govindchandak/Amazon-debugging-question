import random

from django.utils import timezone

from .models import Locker, Parcel

SIZE_RANK = {"S": 1, "M": 2, "L": 3}
PICKUP_WINDOW_DAYS = 3


class LockerError(Exception):
    def __init__(self, message, status):
        super().__init__(message)
        self.status = status


def find_locker_for(size):
    """Smallest free locker that the parcel fits in (S < M < L)."""
    candidates = [locker for locker in Locker.objects.filter(is_free=True) if locker.size >= size]
    if not candidates:
        return None
    return min(candidates, key=lambda locker: (SIZE_RANK[locker.size], locker.id))


def deposit(tracking_id, size):
    if size not in SIZE_RANK:
        raise LockerError("Size must be S, M or L", 400)

    locker = find_locker_for(size)
    if locker is None:
        raise LockerError("No free locker for this size", 409)

    parcel = Parcel.objects.create(
        tracking_id=tracking_id,
        size=size,
        locker=locker,
        pickup_code=f"{random.randint(0, 999999):06d}",
    )
    locker.is_free = False
    locker.save()
    return parcel


def pickup(tracking_id, code):
    parcel = Parcel.objects.filter(tracking_id=tracking_id).select_related("locker").first()
    if parcel is None:
        raise LockerError("Parcel not found", 404)
    if parcel.status != Parcel.IN_LOCKER:
        raise LockerError("Parcel already picked up", 409)
    if parcel.pickup_code != code:
        raise LockerError("Wrong pickup code", 403)

    days_in_locker = (timezone.now() - parcel.deposited_at).days
    if days_in_locker > PICKUP_WINDOW_DAYS:
        raise LockerError("Pickup window has expired", 410)

    parcel.status = Parcel.PICKED_UP
    parcel.save()
    parcel.locker.is_free = True
    return parcel


def free_lockers_count(size):
    return sum(
        1 for locker in Locker.objects.filter(is_free=True)
        if SIZE_RANK[locker.size] >= SIZE_RANK[size]
    )
