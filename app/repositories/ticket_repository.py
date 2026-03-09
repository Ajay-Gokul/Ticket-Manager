from sqlalchemy.orm import Session
from uuid import UUID
from app.models.db_models import Ticket
from app.models.schemas import TicketCreate, TicketUpdate

class TicketRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_ticket_by_id(self, ticket_id: UUID) -> Ticket | None:
        return self.db.query(Ticket).filter(Ticket.UID == ticket_id).first()

    def get_all_tickets(self):
        return self.db.query(Ticket).all()

    def get_unassigned_tickets(self):
        return self.db.query(Ticket).filter(Ticket.AssigneeUID == None).all()

    def get_tickets_by_creator(self, user_id: UUID):
        return self.db.query(Ticket).filter(Ticket.CreatorUID == user_id).all()

    def get_tickets_by_assignee(self, user_id: UUID):
        return self.db.query(Ticket).filter(Ticket.AssigneeUID == user_id).all()

    def create_ticket(self, ticket_in: TicketCreate, creator_uid: UUID) -> Ticket:
        db_ticket = Ticket(
            Title=ticket_in.Title,
            Description=ticket_in.Description,
            StatusUID='A53C14A8-F113-46EF-A634-269484A1AABE', # 'Open' status UID
            Priority=ticket_in.Priority,
            CreatorUID=creator_uid,
            AssigneeUID=None
        )
        self.db.add(db_ticket)
        self.db.commit()
        self.db.refresh(db_ticket)
        return db_ticket

    def update_ticket(self, db_ticket: Ticket, ticket_update: TicketUpdate) -> Ticket:
        update_data = ticket_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_ticket, key, value)
        
        self.db.commit()
        self.db.refresh(db_ticket)
        return db_ticket

    def delete_ticket(self, db_ticket: Ticket):
        self.db.delete(db_ticket)
        self.db.commit()
