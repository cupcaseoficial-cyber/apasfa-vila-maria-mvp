from datetime import date, datetime
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field

class AnimalStatus(str, Enum):
    acolhido = "acolhido"
    tratamento = "tratamento"
    adoção = "adoção"

class StockCategory(str, Enum):
    medicamento = "medicamento"
    insumo = "insumo"

class AnimalBase(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    species: str = Field(min_length=2, max_length=30)
    sex: str = Field(min_length=1, max_length=20)
    status: AnimalStatus = AnimalStatus.acolhido
    birth_date: date | None = None
    allergies: str | None = Field(default=None, max_length=300)

class AnimalCreate(AnimalBase):
    clinical_notes: str = Field(default="", max_length=2000)

class Animal(AnimalBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    clinical_notes: str
    last_updated: datetime

class StockItemBase(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    category: StockCategory
    unit: str = Field(min_length=1, max_length=30)
    quantity: float = Field(ge=0)
    minimum_quantity: float = Field(ge=0)
    expiration_date: date | None = None

class StockItemCreate(StockItemBase):
    pass

class StockItem(StockItemBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    updated_at: datetime

class StockAdjustment(BaseModel):
    quantity_delta: float = Field(description="Quantidade positiva para entrada ou negativa para baixa")
    reason: str = Field(min_length=3, max_length=200)

class LoginRequest(BaseModel):
    email: str
    password: str = Field(min_length=8, max_length=128)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
