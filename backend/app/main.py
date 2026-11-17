from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from . import store
from .models import Animal, AnimalCreate, LoginRequest, StockAdjustment, StockItem, StockItemCreate, TokenResponse
from .security import authenticate_demo_user, create_access_token, get_current_user

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(title="APASFA Vila Maria API", version="0.1.0", description="MVP acadêmico para cuidado clínico e estoque.", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:4200"], allow_credentials=False, allow_methods=["GET", "POST", "PATCH"], allow_headers=["Authorization", "Content-Type"])

@app.get("/api/health", tags=["sistema"])
def health(): return {"status": "ok", "service": "apasfa-api"}

@app.post("/api/auth/login", response_model=TokenResponse, tags=["autenticação"])
def login(payload: LoginRequest):
    if not authenticate_demo_user(payload.email, payload.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="E-mail ou senha inválidos")
    return TokenResponse(access_token=create_access_token(payload.email))

@app.get("/api/animals", response_model=list[Animal], tags=["prontuários"])
def read_animals(_: str = Depends(get_current_user)): return store.list_animals()

@app.get("/api/animals/{animal_id}", response_model=Animal, tags=["prontuários"])
def read_animal(animal_id: int, _: str = Depends(get_current_user)):
    animal = store.get_animal(animal_id)
    if not animal: raise HTTPException(status_code=404, detail="Animal não encontrado")
    return animal

@app.post("/api/animals", response_model=Animal, status_code=201, tags=["prontuários"])
def add_animal(payload: AnimalCreate, _: str = Depends(get_current_user)): return store.create_animal(payload)

@app.get("/api/stock", response_model=list[StockItem], tags=["estoque"])
def read_stock(_: str = Depends(get_current_user)): return store.list_stock()

@app.post("/api/stock", response_model=StockItem, status_code=201, tags=["estoque"])
def add_stock(payload: StockItemCreate, _: str = Depends(get_current_user)): return store.create_stock(payload)

@app.patch("/api/stock/{item_id}/adjust", response_model=StockItem, tags=["estoque"])
def update_stock(item_id: int, payload: StockAdjustment, _: str = Depends(get_current_user)):
    try: item = store.adjust_stock(item_id, payload)
    except ValueError as exc: raise HTTPException(status_code=422, detail=str(exc)) from exc
    if not item: raise HTTPException(status_code=404, detail="Item não encontrado")
    return item
