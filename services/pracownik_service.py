from repo.db import query_db

def get_pracownik(id_pracownika):
    user = query_db('''
        SELECT p.imie, p.nazwisko 
        FROM pracownicy p
        WHERE p.id_pracownika = ?
    ''', (id_pracownika,), one=True)

    return user if user else None