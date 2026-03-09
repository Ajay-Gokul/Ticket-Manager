from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from uuid import UUID
from app.db.database import get_db
from app.models.schemas import TicketCreate, TicketUpdate, TicketResponse
from app.services.ticket_service import TicketService
from app.api.deps import get_current_user
from app.models.db_models import User
from app.core.constants import STATUS_IN_PROGRESS
from typing import List

router = APIRouter()

@router.post("/", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
def create_ticket(ticket_in: TicketCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    ticket_service = TicketService(db)
    return ticket_service.create_new_ticket(ticket_in, current_user.UID)

@router.get("/my-tickets", response_model=List[TicketResponse])
def get_my_tickets(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    ticket_service = TicketService(db)
    return ticket_service.list_tickets_by_creator(current_user.UID)

@router.get("/unassigned", response_model=List[TicketResponse])
def get_unassigned_tickets(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Only admins should ideally see this, but for now we filter in service
    ticket_service = TicketService(db)
    return ticket_service.list_unassigned_tickets()

@router.get("/my-tasks", response_model=List[TicketResponse])
def get_my_tasks(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    ticket_service = TicketService(db)
    return ticket_service.list_tickets_by_assignee(current_user.UID)

@router.put("/{ticket_id}/assign-to-me", response_model=TicketResponse)
def assign_to_me(ticket_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    ticket_service = TicketService(db)
    # Update both the assignee and the status to 'Active'
    update_data = TicketUpdate(
        AssigneeUID=current_user.UID,
        StatusUID=STATUS_IN_PROGRESS
    )
    return ticket_service.update_existing_ticket(ticket_id, update_data)

@router.get("/{ticket_id}", response_model=TicketResponse)
def read_ticket(ticket_id: UUID, db: Session = Depends(get_db)):
    ticket_service = TicketService(db)
    return ticket_service.get_ticket(ticket_id)

@router.put("/{ticket_id}", response_model=TicketResponse)
def update_ticket(ticket_id: UUID, ticket_update: TicketUpdate, db: Session = Depends(get_db)):
    ticket_service = TicketService(db)
    return ticket_service.update_existing_ticket(ticket_id, ticket_update)
