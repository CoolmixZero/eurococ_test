import pytest
from fastapi import HTTPException

from models import Vozidlo, NewVozidlo
from database import get_db_connection
from v1.routes.cars import create_vozidlo, delete_vozidlo, get_all_vozidla, get_vozidlo, update_vozidlo


@pytest.fixture()
def db_connection():
    connection = get_db_connection()
    yield connection
    connection.close()


# Test for GET /vozidla
@pytest.mark.asyncio
async def test_get_all_vozidla(db_connection):
    # Simulate a successful GET request
    response = await get_all_vozidla(db_connection=db_connection)

    # Check if the response is a list of Vozidlo objects
    assert isinstance(response, list)
    for vozidlo in response:
        assert isinstance(vozidlo, Vozidlo)
        vozidlo = vozidlo.model_dump()
        assert "id" in vozidlo
        assert "Kategoria_vozidla" in vozidlo
        assert "Znacka_vozidla" in vozidlo
        assert "Predajna_cena" in vozidlo
        assert "Datum_vytvorenia" in vozidlo
        assert "Stav" in vozidlo


# Test for POST /vozidla
@pytest.mark.asyncio
async def test_create_vozidlo(db_connection):
    # Create a new Vozidlo object
    new_vozidlo = NewVozidlo(
        Kategoria_vozidla="PKW",
        Znacka_vozidla="Audi",
        Predajna_cena=500,
        Datum_vytvorenia="2024-01-01",
        Stav="Vybavene",
    )

    # Simulate a successful POST request
    response = await create_vozidlo(vozidlo=new_vozidlo.model_dump(), db_connection=db_connection)

    # Check if the response is a Vozidlo object
    assert isinstance(response, Vozidlo)
    
    assert "id" in response.model_dump()
    assert response.Kategoria_vozidla == new_vozidlo.Kategoria_vozidla
    assert response.Znacka_vozidla == new_vozidlo.Znacka_vozidla
    assert response.Predajna_cena == new_vozidlo.Predajna_cena
    assert response.Datum_vytvorenia == new_vozidlo.Datum_vytvorenia
    assert response.Stav == new_vozidlo.Stav


# Test for GET /vozidla/{vozidlo_id}
@pytest.mark.asyncio
async def test_get_vozidlo_by_id(db_connection):
    # Create a new Vozidlo object and insert it into the database
    new_vozidlo = NewVozidlo(
        Kategoria_vozidla="PKW",
        Znacka_vozidla="Audi",
        Predajna_cena=500,
        Datum_vytvorenia="2024-01-01",
        Stav="Vybavene",
    )
    new_vozidlo = await create_vozidlo(vozidlo=new_vozidlo.model_dump(), db_connection=db_connection)

    vozidlo_id = new_vozidlo.id
    # Simulate a successful GET request with the ID
    response = await get_vozidlo(vozidlo_id=vozidlo_id, db_connection=db_connection)

    # Check if the response is a Vozidlo object and matches the inserted data
    assert isinstance(response, Vozidlo)
    assert response.id == vozidlo_id
    assert response.Kategoria_vozidla == new_vozidlo.Kategoria_vozidla
    assert response.Znacka_vozidla == new_vozidlo.Znacka_vozidla
    assert response.Predajna_cena == new_vozidlo.Predajna_cena
    assert response.Datum_vytvorenia == new_vozidlo.Datum_vytvorenia
    assert response.model_dump_json()

# Test for GET /vozidla/{vozidlo_id} Not Found
@pytest.mark.asyncio
async def test_get_vozidlo_by_id_not_found(db_connection):
    # Simulate a GET request with a non-existent ID
    invalid_id = "1234"
    with pytest.raises(HTTPException) as excinfo:
        await get_vozidlo(vozidlo_id=invalid_id, db_connection=db_connection)
    assert excinfo.value.status_code == 404


# Test for PUT /vozidla/{vozidlo_id}
@pytest.mark.asyncio
async def test_update_vozidlo(db_connection):
    # Create a new Vozidlo object and insert it into the database
    new_vozidlo = NewVozidlo(
        Kategoria_vozidla="PKW",
        Znacka_vozidla="Audi",
        Predajna_cena=500,
        Datum_vytvorenia="2024-01-01",
        Stav="Vybavene",
    )
    new_vozidlo = await create_vozidlo(vozidlo=new_vozidlo.model_dump(), db_connection=db_connection)
    
    # Update data for the Vozidlo
    updated_vozidlo = NewVozidlo(
        Kategoria_vozidla="Motocykel",
        Znacka_vozidla="BMW",
        Predajna_cena=700,
        Datum_vytvorenia="2023-12-31",
        Stav="Rezervovane",
    )

    vozidlo_id = new_vozidlo.id
    
    # Simulate a successful PUT request
    response = await update_vozidlo(vozidlo_id=vozidlo_id, new_vozidlo=updated_vozidlo, db_connection=db_connection)

    # Check if the response is a Vozidlo object with the updated data
    assert isinstance(response, Vozidlo)
    assert response.id == vozidlo_id
    assert response.Kategoria_vozidla == updated_vozidlo.Kategoria_vozidla
    assert response.Znacka_vozidla == updated_vozidlo.Znacka_vozidla
    assert response.Predajna_cena == updated_vozidlo.Predajna_cena
    assert response.Datum_vytvorenia == updated_vozidlo.Datum_vytvorenia
    assert response.Stav == updated_vozidlo.Stav


# Test for PUT /vozidla/{vozidlo_id} - Not Found
@pytest.mark.asyncio
async def test_update_vozidlo_not_found(db_connection):
    # Simulate a PUT request with a non-existent ID
    invalid_id = "1234"
    updated_vozidlo = NewVozidlo(
        Kategoria_vozidla="Motocykel",
        Znacka_vozidla="BMW",
        Predajna_cena=700,
        Datum_vytvorenia="2023-12-31",
        Stav="Rezervovane",
    )
    with pytest.raises(HTTPException) as excinfo:
        await update_vozidlo(vozidlo_id=invalid_id, new_vozidlo=updated_vozidlo, db_connection=db_connection)
    assert excinfo.value.status_code == 404

@pytest.mark.asyncio
async def test_delete_vozidlo(db_connection):
    # Create a new Vozidlo object and insert it into the database
    new_vozidlo = NewVozidlo(
        Kategoria_vozidla="PKW",
        Znacka_vozidla="Audi",
        Predajna_cena=500,
        Datum_vytvorenia="2024-01-01",
        Stav="Vybavene",
    )
    new_vozidlo = await create_vozidlo(vozidlo=new_vozidlo.model_dump(), db_connection=db_connection)

    vozidlo_id = new_vozidlo.id
    
    # Simulate a successful DELETE request
    await delete_vozidlo(vozidlo_id=vozidlo_id, db_connection=db_connection)

    # Try to get the deleted Vozidlo by ID (should raise 404)
    with pytest.raises(HTTPException) as excinfo:
        await get_vozidlo(vozidlo_id=vozidlo_id, db_connection=db_connection)
    assert excinfo.value.status_code == 404


# Test for DELETE /vozidla/{vozidlo_id} - Not Found
@pytest.mark.asyncio
async def test_delete_vozidlo_not_found(db_connection):
    # Simulate a DELETE request with a non-existent ID
    invalid_id = "1234"
    with pytest.raises(HTTPException) as excinfo:
        await delete_vozidlo(vozidlo_id=invalid_id, db_connection=db_connection)
    assert excinfo.value.status_code == 404