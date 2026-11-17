from datetime import date, datetime, timezone
from .models import Animal, AnimalCreate, StockAdjustment, StockItem, StockItemCreate

_animals = {
    1: Animal(id=1, name="Luna", species="Cão", sex="Fêmea", status="tratamento", birth_date=date(2021, 5, 12), allergies="Nenhuma conhecida", clinical_notes="Curativo na pata traseira; reavaliar em 20/11.", last_updated=datetime.now(timezone.utc)),
    2: Animal(id=2, name="Mingau", species="Gato", sex="Macho", status="acolhido", birth_date=date(2022, 8, 2), allergies=None, clinical_notes="Vacinação em dia.", last_updated=datetime.now(timezone.utc)),
}
_stock = {
    1: StockItem(id=1, name="Antisséptico", category="medicamento", unit="frascos", quantity=3, minimum_quantity=5, expiration_date=date(2027, 2, 1), updated_at=datetime.now(timezone.utc)),
    2: StockItem(id=2, name="Gaze estéril", category="insumo", unit="pacotes", quantity=18, minimum_quantity=10, expiration_date=None, updated_at=datetime.now(timezone.utc)),
}

def list_animals() -> list[Animal]: return list(_animals.values())
def get_animal(animal_id: int) -> Animal | None: return _animals.get(animal_id)
def create_animal(data: AnimalCreate) -> Animal:
    next_id = max(_animals, default=0) + 1
    animal = Animal(id=next_id, **data.model_dump(), last_updated=datetime.now(timezone.utc))
    _animals[next_id] = animal
    return animal

def list_stock() -> list[StockItem]: return list(_stock.values())
def get_stock(item_id: int) -> StockItem | None: return _stock.get(item_id)
def create_stock(data: StockItemCreate) -> StockItem:
    next_id = max(_stock, default=0) + 1
    item = StockItem(id=next_id, **data.model_dump(), updated_at=datetime.now(timezone.utc))
    _stock[next_id] = item
    return item

def adjust_stock(item_id: int, adjustment: StockAdjustment) -> StockItem | None:
    item = _stock.get(item_id)
    if not item: return None
    new_quantity = item.quantity + adjustment.quantity_delta
    if new_quantity < 0: raise ValueError("A baixa não pode deixar o estoque negativo")
    updated = item.model_copy(update={"quantity": new_quantity, "updated_at": datetime.now(timezone.utc)})
    _stock[item_id] = updated
    return updated
