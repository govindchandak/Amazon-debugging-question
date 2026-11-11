from .errors import HttpError
from .models import Reply, Ticket

PAGE_SIZE = 5


def summary(ticket):
    return {"id": ticket.id, "title": ticket.title, "owner": ticket.owner, "status": ticket.status}


def create_ticket(title, description, user):
    ticket = Ticket.objects.create(title=title, description=description, owner=user.name)
    return summary(ticket)


def list_tickets(user, page):
    """Customers see only their own tickets. Agents see all. Newest first, 5 per page."""
    tickets = Ticket.objects.all() if user.role == "AGENT" else Ticket.objects.filter(owner=user.name)
    tickets = tickets.order_by("-id")
    start = page * PAGE_SIZE
    return [summary(t) for t in tickets[start:start + PAGE_SIZE]]


def find_visible_ticket(ticket_id, user):
    """Loads a ticket the user is allowed to see."""
    ticket = Ticket.objects.get(id=ticket_id)
    return ticket


def get_ticket(ticket_id, user):
    ticket = find_visible_ticket(ticket_id, user)
    replies = [{"author": r.author, "message": r.message} for r in ticket.replies.order_by("id")]
    return {**summary(ticket), "description": ticket.description, "replies": replies}


def add_reply(ticket_id, message, user):
    ticket = find_visible_ticket(ticket_id, user)
    if not message or not message.strip():
        raise HttpError(400, "Message is required")
    reply = Reply(ticket=ticket, author=user.name, message=message.strip())
    return {"author": reply.author, "message": reply.message}


def change_status(ticket_id, new_status, user):
    if user.role != "AGENT":
        raise HttpError(403, "Only agents can change status")
    if new_status not in Ticket.STATUSES:
        raise HttpError(400, "Status must be one of " + ", ".join(Ticket.STATUSES))
    ticket = Ticket.objects.filter(id=ticket_id).first()
    if ticket is None:
        raise HttpError(404, "Ticket not found")
    ticket.status = new_status
    ticket.save()
    return summary(ticket)


def count_replies_from_others(user):
    """How many replies on my tickets were written by someone else."""
    return Reply.objects.filter(ticket__owner=user.name).count()
