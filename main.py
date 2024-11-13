from fastapi import FastAPI
from routers import transaction_router
from models.models import Base, engine
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(transaction_router.router, prefix="/transactions", tags=["transactions"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Banking Transfer API"}
