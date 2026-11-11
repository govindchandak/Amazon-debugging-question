import json

from django.test import TestCase

from .models import Reply, Ticket


class HelpDeskTests(TestCase):
    def call(self, method, url, user=None, data=None):
        headers = {"X-User": user} if user else {}
        send = getattr(self.client, method)
        if data is None:
            return send(url, headers=headers)
        return send(url, data=json.dumps(data), content_type="application/json", headers=headers)

    def create_ticket(self, user, title="Order not delivered"):
        return self.call("post", "/api/tickets", user, {"title": title, "description": "Details"}).json()

    # ---------- who is calling ----------

    def test_request_without_user_header_returns_401(self):
        self.assertEqual(self.call("get", "/api/tickets").status_code, 401)

    def test_unknown_user_returns_401(self):
        self.assertEqual(self.call("get", "/api/tickets", "hacker").status_code, 401)

    # ---------- create ticket ----------

    def test_create_ticket_returns_201_with_status_open(self):
        response = self.call("post", "/api/tickets", "asha", {"title": "Refund missing"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["owner"], "asha")
        self.assertEqual(response.json()["status"], "OPEN")

    def test_blank_title_returns_400(self):
        response = self.call("post", "/api/tickets", "asha", {"title": "   "})
        self.assertEqual(response.status_code, 400)

    # ---------- view ticket ----------

    def test_owner_can_view_their_ticket(self):
        ticket = self.create_ticket("asha")
        response = self.call("get", f"/api/tickets/{ticket['id']}", "asha")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], "Order not delivered")

    def test_another_customer_gets_403(self):
        ticket = self.create_ticket("asha")
        response = self.call("get", f"/api/tickets/{ticket['id']}", "ravi")
        self.assertEqual(response.status_code, 403)

    def test_agent_can_view_any_ticket(self):
        ticket = self.create_ticket("asha")
        response = self.call("get", f"/api/tickets/{ticket['id']}", "neha")
        self.assertEqual(response.status_code, 200)

    def test_unknown_ticket_returns_404(self):
        response = self.call("get", "/api/tickets/99", "asha")
        self.assertEqual(response.status_code, 404)

    # ---------- replies ----------

    def test_reply_is_saved_and_shown_on_the_ticket(self):
        ticket = self.create_ticket("asha")
        url = f"/api/tickets/{ticket['id']}"
        response = self.call("post", url + "/replies", "neha", {"message": "Checking with courier"})
        self.assertEqual(response.status_code, 201)

        replies = self.call("get", url, "asha").json()["replies"]
        self.assertEqual(replies, [{"author": "neha", "message": "Checking with courier"}])

    def test_blank_reply_returns_400(self):
        ticket = self.create_ticket("asha")
        response = self.call("post", f"/api/tickets/{ticket['id']}/replies", "neha", {"message": ""})
        self.assertEqual(response.status_code, 400)

    # ---------- change status ----------

    def test_agent_can_move_ticket_to_in_progress(self):
        ticket = self.create_ticket("asha")
        response = self.call("patch", f"/api/tickets/{ticket['id']}/status", "neha", {"status": "IN_PROGRESS"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "IN_PROGRESS")

    def test_customer_cannot_change_status(self):
        ticket = self.create_ticket("asha")
        response = self.call("patch", f"/api/tickets/{ticket['id']}/status", "asha", {"status": "CLOSED"})
        self.assertEqual(response.status_code, 403)

    def test_closed_ticket_cannot_change_status(self):
        ticket = self.create_ticket("asha")
        url = f"/api/tickets/{ticket['id']}/status"
        self.call("patch", url, "neha", {"status": "CLOSED"})
        response = self.call("patch", url, "neha", {"status": "OPEN"})
        self.assertEqual(response.status_code, 409)

    # ---------- list tickets ----------

    def test_customer_sees_only_their_own_tickets(self):
        self.create_ticket("asha", "A1")
        self.create_ticket("ravi", "R1")
        titles = [t["title"] for t in self.call("get", "/api/tickets", "ravi").json()]
        self.assertEqual(titles, ["R1"])

    def test_five_per_page_newest_first(self):
        for i in range(1, 7):
            self.create_ticket("asha", f"T{i}")
        page1 = [t["title"] for t in self.call("get", "/api/tickets?page=1", "asha").json()]
        page2 = [t["title"] for t in self.call("get", "/api/tickets?page=2", "asha").json()]
        self.assertEqual(page1, ["T6", "T5", "T4", "T3", "T2"])
        self.assertEqual(page2, ["T1"])

    # ---------- notifications ----------

    def test_count_includes_only_replies_from_others(self):
        ticket = Ticket.objects.create(title="Late order", owner="asha")
        Reply.objects.create(ticket=ticket, author="asha", message="Any update?")
        Reply.objects.create(ticket=ticket, author="neha", message="Arriving today")
        response = self.call("get", "/api/notifications/count", "asha")
        self.assertEqual(response.json()["count"], 1)
