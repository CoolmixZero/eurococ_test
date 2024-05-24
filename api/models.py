from pydantic import BaseModel


class Vozidlo(BaseModel):
    id: int
    Kategoria_vozidla: str
    Znacka_vozidla: str
    Predajna_cena: float
    Datum_vytvorenia: str
    Stav: str
    
    
class NewVozidlo(BaseModel):
    Kategoria_vozidla: str
    Znacka_vozidla: str
    Predajna_cena: float
    Datum_vytvorenia: str
    Stav: str