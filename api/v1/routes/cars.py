import sys
from fastapi import APIRouter, HTTPException, status, Depends, Body
from mysql.connector import MySQLConnection
from typing import List
sys.path.append("api")
from models import Vozidlo, NewVozidlo
from database import get_db_connection


router = APIRouter(
    prefix="/vozidla",
    tags=["vozidla"]
)

# # In-memory data storage (replace with database later)
# VOZIDLA = [ 
#     {"id": generate_id(),"Kategoria_vozidla": 'LKW', "Znacka_vozidla": 'BMW', "Predajna_cena": 100, "Datum_vytvorenia": '2020-01-01', "Stav": 'Stornovane' },
#     {"id": generate_id(), "Kategoria_vozidla": 'LKW', "Znacka_vozidla": 'AUDI', "Predajna_cena": 200, "Datum_vytvorenia": '2021-01-01', "Stav": 'Vybavene' },
#     {"id": generate_id(), "Kategoria_vozidla": 'PKW', "Znacka_vozidla": 'VW', "Predajna_cena": 300, "Datum_vytvorenia": '2022-01-01', "Stav": 'Vybavene' },
#     {"id": generate_id(), "Kategoria_vozidla": 'LKW', "Znacka_vozidla": 'MERCEDES', "Predajna_cena": 400, "Datum_vytvorenia": '2023-01-01', "Stav": 'Vybavuje sa' }
# ]

@router.get("/", response_model=List[Vozidlo])
async def get_all_vozidla(db_connection: MySQLConnection = Depends(get_db_connection)):
    cursor = db_connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Vozidla")
    result = cursor.fetchall()
    cursor.close()
    return [Vozidlo(**vozidlo) for vozidlo in result]

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Vozidlo)
async def create_vozidlo(vozidlo: dict = Body(), db_connection: MySQLConnection = Depends(get_db_connection)):    
    vozidlo = NewVozidlo(**vozidlo)
    vozidlo.Datum_vytvorenia = str(vozidlo.Datum_vytvorenia).split("T")[0]
    
    cursor = db_connection.cursor()
    cursor.execute(
        "INSERT INTO Vozidla (Kategoria_vozidla, Znacka_vozidla, Predajna_cena, Datum_vytvorenia, Stav) VALUES (%s, %s, %s, %s, %s)",
        (vozidlo.Kategoria_vozidla, vozidlo.Znacka_vozidla, vozidlo.Predajna_cena, vozidlo.Datum_vytvorenia, vozidlo.Stav)
    )
    vozidlo_id = cursor.lastrowid 
    db_connection.commit()
    cursor.close()

    return Vozidlo(id=vozidlo_id, **vozidlo.model_dump())

@router.get("/{vozidlo_id}", response_model=Vozidlo)
async def get_vozidlo(vozidlo_id: str, db_connection: MySQLConnection = Depends(get_db_connection)):
    cursor = db_connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Vozidla WHERE id = %s", (vozidlo_id,))
    result = cursor.fetchone()  
    cursor.close()

    if not result:
        raise HTTPException(status_code=404, detail="Vozidlo not found")

    return Vozidlo(**result)

@router.put("/{vozidlo_id}", response_model=Vozidlo)
async def update_vozidlo(vozidlo_id: str, new_vozidlo: NewVozidlo, db_connection: MySQLConnection = Depends(get_db_connection)):
    cursor = db_connection.cursor()
    
    query = "UPDATE Vozidla SET Kategoria_vozidla = %s, Znacka_vozidla = %s, Predajna_cena = %s, Datum_vytvorenia = %s, Stav = %s WHERE id = %s"
    cursor.execute(
        query,
        (new_vozidlo.Kategoria_vozidla, new_vozidlo.Znacka_vozidla, new_vozidlo.Predajna_cena, new_vozidlo.Datum_vytvorenia, new_vozidlo.Stav, vozidlo_id)
    )
    db_connection.commit()  # Commit the changes
    cursor.close()
    
    # Fetch and return the updated Vozidlo
    cursor = db_connection.cursor(dictionary=True)
    query = "SELECT * FROM Vozidla WHERE id = %s"
    cursor.execute(query, (vozidlo_id,))
    result = cursor.fetchone()
    cursor.close()
    if not result:
        raise HTTPException(status_code=404, detail="Vozidlo not found after update")

    return Vozidlo(**result)

@router.delete("/{vozidlo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_vozidlo(vozidlo_id: str, db_connection: MySQLConnection = Depends(get_db_connection)):
    cursor = db_connection.cursor()
    query = "DELETE FROM Vozidla WHERE id = %s"
    cursor.execute(query, (vozidlo_id,))
    db_connection.commit()
    cursor.close()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Vozidlo not found")