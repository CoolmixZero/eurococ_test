from datetime import date  
from pydantic import BaseModel, Field


class Vozidlo(BaseModel):
    id: int
    Kategoria_vozidla: str
    Znacka_vozidla: str
    Predajna_cena: float
    Datum_vytvorenia: date
    Stav: str
    
    
class NewVozidlo(BaseModel):
    Kategoria_vozidla: str
    Znacka_vozidla: str
    Predajna_cena: float
    Datum_vytvorenia: date  # Use datetime for dates
    Stav: str