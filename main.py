# main.py
from fastapi import FastAPI
from routers import transaction_router
from models.models import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routers
app.include_router(transaction_router.router, prefix="/transactions", tags=["transactions"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Banking Transfer API"}
