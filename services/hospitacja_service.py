from repo.db import query_db

def get_hospitacje_pracownika(id_pracownika):
    hospitacje = query_db('''
        SELECT h.id_hospitacji, h.termin, h.data_zatwierdzenia, p.nazwa
        FROM hospitacje h
        JOIN przedmioty p ON h.przedmiot_id = p.id_przedmiotu
        WHERE h.hospitowany_id = ? AND h.data_sporzadzenia IS NOT NULL
        ORDER BY h.termin DESC
    ''', (id_pracownika,))
    
    return [
        {
            'id': h['id_hospitacji'],
            'termin': h['termin'],
            'status': 'completed' if h['data_zatwierdzenia'] else 'pending',
            'nazwa': h['nazwa']
        } for h in hospitacje
    ]

def get_hospitacja_details(id_hospitacji):
    query = '''
    SELECT 
        p.nazwa AS przedmiot_nazwa,
        p.kod AS przedmiot_kod,
        h.termin,
        h.miejsce,
        h.zawartosc_protokolu AS protokol,
        h.data_zatwierdzenia,
        GROUP_CONCAT(pracownicy.imie || ' ' || pracownicy.nazwisko) AS zespol_hospitujacy
    FROM hospitacje h
    JOIN przedmioty p ON h.przedmiot_id = p.id_przedmiotu
    LEFT JOIN zespoly_hospitujace zh ON h.id_hospitacji = zh.id_hospitacji
    LEFT JOIN pracownicy ON pracownicy.id_pracownika = zh.id_hospitujacego
    WHERE h.id_hospitacji = ?
    GROUP BY h.id_hospitacji
    '''
    
    hospitacja = query_db(query, (id_hospitacji,), one=True)
    
    if not hospitacja:
        return None
    
    return {
        'przedmiot_nazwa': hospitacja['przedmiot_nazwa'],
        'przedmiot_kod': hospitacja['przedmiot_kod'],
        'termin': hospitacja['termin'],
        'miejsce': hospitacja['miejsce'],
        'protokol': hospitacja['protokol'],
        'zespol_hospitujacy': hospitacja['zespol_hospitujacy'].split(',') if hospitacja['zespol_hospitujacy'] else [],
        'status': 'completed' if hospitacja['data_zatwierdzenia'] else 'pending'
    }

def zaakceptuj_hospitacje(id_hospitacji):
    query_db('''
        UPDATE hospitacje
        SET data_zatwierdzenia = CURRENT_TIMESTAMP
        WHERE id_hospitacji = ?
    ''', (id_hospitacji,))
    return {'message': 'Hospitacja została zaakceptowana'}