from fastapi import FastAPI
from routers import transaction_router, login_router, purchase_router, customer_router
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
app.include_router(login_router.router, prefix="/auth", tags=["auth"])
app.include_router(purchase_router.router, tags=["purchase"])
app.include_router(customer_router.router, tags=["customer"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Banking Transfer API"}