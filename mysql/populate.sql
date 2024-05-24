use db;

-- Create the table (no changes needed here)
CREATE TABLE Vozidla (
    id INT NOT NULL AUTO_INCREMENT,
    Kategoria_vozidla VARCHAR(255),
    Znacka_vozidla VARCHAR(255),
    Predajna_cena DECIMAL(10, 2),
    Datum_vytvorenia VARCHAR(255),
    Stav VARCHAR(255),
    PRIMARY KEY (id)
);

INSERT INTO Vozidla (Kategoria_vozidla, Znacka_vozidla, Predajna_cena, Datum_vytvorenia, Stav)
VALUES 
    ('LKW', 'BMW', 100, '2020-01-01', 'Stornovane'),
    ('LKW', 'AUDI', 200, '2021-01-01', 'Vybavene'),
    ('PKW', 'VW', 300, '2022-01-01', 'Vybavene'),
    ('LKW', 'MERCEDES', 400, '2023-01-01', 'Vybavuje sa');
