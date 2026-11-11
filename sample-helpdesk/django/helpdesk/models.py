from django.db import models


class Ticket(models.Model):
    STATUSES = ["OPEN", "IN_PROGRESS", "RESOLVED", "CLOSED"]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    owner = models.CharField(max_length=50)
    status = models.CharField(max_length=20, default="OPEN")


class Reply(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="replies")
    author = models.CharField(max_length=50)
    message = models.TextField()
