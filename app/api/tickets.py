from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from uuid import UUID
from app.db.database import get_db
from app.models.schemas import TicketCreate, TicketUpdate, TicketResponse
from app.services.ticket_service import TicketService
from typing import List

router = APIRouter()

@router.post("/", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
def create_ticket(ticket_in: TicketCreate, db: Session = Depends(get_db)):
    ticket_service = TicketService(db)
    return ticket_service.create_new_ticket(ticket_in)

@router.get("/{ticket_id}", response_model=TicketResponse)
def read_ticket(ticket_id: UUID, db: Session = Depends(get_db)):
    ticket_service = TicketService(db)
    return ticket_service.get_ticket(ticket_id)

@router.get("/", response_model=List[TicketResponse])
def read_tickets(db: Session = Depends(get_db)):
    ticket_service = TicketService(db)
    return ticket_service.list_all_tickets()

@router.put("/{ticket_id}", response_model=TicketResponse)
def update_ticket(ticket_id: UUID, ticket_update: TicketUpdate, db: Session = Depends(get_db)):
    ticket_service = TicketService(db)
    return ticket_service.update_existing_ticket(ticket_id, ticket_update)

@router.delete("/{ticket_id}")
def delete_ticket(ticket_id: UUID, db: Session = Depends(get_db)):
    ticket_service = TicketService(db)
    return ticket_service.remove_ticket(ticket_id)
