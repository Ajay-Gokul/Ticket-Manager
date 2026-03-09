from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api import auth, tickets
from app.core.exceptions import BaseAppException

app = FastAPI(title="Ticket Manager API")

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Exception Handler
@app.exception_handler(BaseAppException)
async def app_exception_handler(request: Request, exc: BaseAppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )

# Generic Exception Handler for unhandled errors
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    # Log the full exception here in production
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred. Please try again later."},
    )

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(tickets.router, prefix="/tickets", tags=["Tickets"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Ticket Manager API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
