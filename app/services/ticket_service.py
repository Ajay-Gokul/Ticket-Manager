from sqlalchemy.orm import Session
from uuid import UUID
from app.repositories.ticket_repository import TicketRepository
from app.models.schemas import TicketCreate, TicketUpdate
from app.core.exceptions import NotFoundException

class TicketService:
    def __init__(self, db: Session):
        self.ticket_repo = TicketRepository(db)

    def create_new_ticket(self, ticket_in: TicketCreate, creator_uid: UUID):
        return self.ticket_repo.create_ticket(ticket_in, creator_uid)

    def get_ticket(self, ticket_id: UUID):
        ticket = self.ticket_repo.get_ticket_by_id(ticket_id)
        if not ticket:
            raise NotFoundException(f"Ticket with UID {ticket_id} not found")
        return ticket

    def list_all_tickets(self):
        return self.ticket_repo.get_all_tickets()

    def list_unassigned_tickets(self):
        return self.ticket_repo.get_unassigned_tickets()

    def list_tickets_by_creator(self, user_id: UUID):
        return self.ticket_repo.get_tickets_by_creator(user_id)

    def list_tickets_by_assignee(self, user_id: UUID):
        return self.ticket_repo.get_tickets_by_assignee(user_id)

    def update_existing_ticket(self, ticket_id: UUID, ticket_update: TicketUpdate):
        db_ticket = self.get_ticket(ticket_id)
        return self.ticket_repo.update_ticket(db_ticket, ticket_update)

    def remove_ticket(self, ticket_id: UUID):
        db_ticket = self.get_ticket(ticket_id)
        self.ticket_repo.delete_ticket(db_ticket)
        return {"msg": "Ticket deleted successfully"}
