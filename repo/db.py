import sqlite3
import os

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def query_db(query, args=(), one=False):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(query, args)
        rv = cur.fetchall()
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        rv = Nonea
    finally:
        conn.close()
    return (rv[0] if rv else None) if one else rv

def create_tables():
    tables = [
        '''CREATE TABLE IF NOT EXISTS semestry (
            id_semestru INTEGER PRIMARY KEY AUTOINCREMENT,
            nazwa_semestru TEXT NOT NULL
        )''',
        '''CREATE TABLE IF NOT EXISTS stopnie_naukowe (
            id_stopnia INTEGER PRIMARY KEY AUTOINCREMENT,
            nazwa_stopnia TEXT NOT NULL
        )''',
        '''CREATE TABLE IF NOT EXISTS pracownicy (
            id_pracownika INTEGER PRIMARY KEY AUTOINCREMENT,
            imie TEXT NOT NULL,
            nazwisko TEXT NOT NULL,
            stopien_naukowy_id INTEGER,
            FOREIGN KEY(stopien_naukowy_id) REFERENCES stopnie_naukowe(id_stopnia)
        )''',
        '''CREATE TABLE IF NOT EXISTS przedmioty (
            id_przedmiotu INTEGER PRIMARY KEY AUTOINCREMENT,
            kod TEXT NOT NULL,
            nazwa TEXT NOT NULL,
            karta_przedmiotu TEXT
        )''',
        '''CREATE TABLE IF NOT EXISTS harmonogramy (
            id_harmonogramu INTEGER PRIMARY KEY AUTOINCREMENT,
            rok_akademicki TEXT NOT NULL,
            semestr_id INTEGER,
            data_sporzadzenia DATE NOT NULL,
            FOREIGN KEY(semestr_id) REFERENCES semestry(id_semestru)
        )''',
        '''CREATE TABLE IF NOT EXISTS przedmioty_pracownikow (
            id_pracownika INTEGER,
            id_przedmiotu INTEGER,
            FOREIGN KEY(id_pracownika) REFERENCES pracownicy(id_pracownika),
            FOREIGN KEY(id_przedmiotu) REFERENCES przedmioty(id_przedmiotu)
        )''',
        '''CREATE TABLE IF NOT EXISTS hospitacje (
            id_hospitacji INTEGER PRIMARY KEY AUTOINCREMENT,
            liczba_osob_zapisanych INTEGER,
            miejsce TEXT,
            termin DATE,
            hospitowany_id INTEGER,
            przedmiot_id INTEGER,
            harmonogram_id INTEGER,
            zawartosc_protokolu TEXT,
            data_sporzadzenia DATE,
            data_zatwierdzenia DATE,
            FOREIGN KEY(hospitowany_id) REFERENCES pracownicy(id_pracownika),
            FOREIGN KEY(przedmiot_id) REFERENCES przedmioty(id_przedmiotu),
            FOREIGN KEY(harmonogram_id) REFERENCES harmonogramy(id_harmonogramu)
        )''',
        '''CREATE TABLE IF NOT EXISTS zespoly_hospitujace (
            id_hospitacji INTEGER,
            id_hospitujacego INTEGER,
            FOREIGN KEY(id_hospitacji) REFERENCES hospitacje(id_hospitacji),
            FOREIGN KEY(id_hospitujacego) REFERENCES pracownicy(id_pracownika)
        )'''
    ]
    
    conn = get_db_connection()
    cur = conn.cursor()
    for table in tables:
        cur.execute(table)
    
    conn.commit()
    conn.close()

def insert_initial_data():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Semestry
    cursor.execute("INSERT INTO semestry (nazwa_semestru) VALUES (?)", ("letni",))
    cursor.execute("INSERT INTO semestry (nazwa_semestru) VALUES (?)", ("zimowy",))

    # Stopnie naukowe
    stopnie = [
        ("licencjat",),
        ("magister",),
        ("inżynier",),
        ("doktor",),
        ("doktor habilitowany",),
        ("profesor",)
    ]
    cursor.executemany("INSERT INTO stopnie_naukowe (nazwa_stopnia) VALUES (?)", stopnie)

    # Pracownicy
    pracownicy = [
        ("Jan", "Kowalski", 1),
        ("Anna", "Nowak", 2),
        ("Piotr", "Zieliński", 3),
        ("Katarzyna", "Wiśniewska", 4),
        ("Tomasz", "Kowal", 5),
        ("Marek", "Szymański", 6),
        ("Łukasz", "Lewandowski", 1),
        ("Patryk", "Wojciechowski", 2),
        ("Magdalena", "Kaczmarek", 3),
        ("Piotr", "Kamiński", 4),
        ("Joanna", "Nowicka", 5),
        ("Krzysztof", "Wójcik", 6),
        ("Aleksandra", "Kowalczyk", 1),
        ("Sebastian", "Lis", 2),
        ("Ewa", "Mazur", 3),
        ("Andrzej", "Jankowski", 4),
        ("Michał", "Zawisza", 5),
        ("Barbara", "Sienkiewicz", 6),
        ("Grzegorz", "Kubiak", 1),
        ("Martyna", "Pawlak", 2)
    ]
    cursor.executemany("INSERT INTO pracownicy (imie, nazwisko, stopien_naukowy_id) VALUES (?, ?, ?)", pracownicy)

    # Przedmioty
    przedmioty = [
        ("W041ST-S10018L", "Techniki efektywnego programowania", "W041ST-S10018L.pdf"),
        ("W041ST-S10019L", "Programowanie obiektowe", "W041ST-S10019L.pdf"),
        ("W041ST-S10020L", "Algorytmy i struktury danych", "W041ST-S10020L.pdf"),
        ("W041ST-S10021L", "Bazy danych", "W041ST-S10021L.pdf"),
        ("W041ST-S10022L", "Sieci komputerowe", "W041ST-S10022L.pdf"),
        ("W041ST-S10023L", "Systemy operacyjne", "W041ST-S10023L.pdf"),
        ("W041ST-S10024L", "Inżynieria oprogramowania", "W041ST-S10024L.pdf"),
        ("W041ST-S10025L", "Teoria grafów", "W041ST-S10025L.pdf"),
        ("W041ST-S10026L", "Programowanie w języku Java", "W041ST-S10026L.pdf"),
        ("W041ST-S10027L", "Analiza algorytmów", "W041ST-S10027L.pdf"),
        ("W041ST-S10028L", "Programowanie w języku Python", "W041ST-S10028L.pdf"),
        ("W041ST-S10029L", "Sztuczna inteligencja", "W041ST-S10029L.pdf"),
        ("W041ST-S10030L", "Inżynieria baz danych", "W041ST-S10030L.pdf"),
        ("W041ST-S10031L", "Programowanie w języku C++", "W041ST-S10031L.pdf"),
        ("W041ST-S10032L", "Bezpieczeństwo komputerowe", "W041ST-S10032L.pdf"),
        ("W041ST-S10033L", "Programowanie mobilne", "W041ST-S10033L.pdf"),
        ("W041ST-S10034L", "Chmura obliczeniowa", "W041ST-S10034L.pdf"),
        ("W041ST-S10035L", "Podstawy zarządzania jakością", "W041ST-S10035L.pdf"),
        ("W041ST-S10036L", "Podstawy prawa w informatyce", "W041ST-S10036L.pdf"),
        ("W041ST-S10037L", "Podstawy ekonomii", "W041ST-S10037L.pdf"),
        ("W041ST-S10038L", "Podstawy matematyki dyskretnej", "W041ST-S10038L.pdf")
    ]
    cursor.executemany("INSERT INTO przedmioty (kod, nazwa, karta_przedmiotu) VALUES (?, ?, ?)", przedmioty)

    # Harmonogramy
    harmonogramy = [
        ("2024/2025", 1, "2024-09-01"),
        ("2024/2025", 2, "2025-02-01"),
        ("2025/2026", 1, "2025-09-01")
    ]
    cursor.executemany("INSERT INTO harmonogramy (rok_akademicki, semestr_id, data_sporzadzenia) VALUES (?, ?, ?)", harmonogramy)

    # Przedmioty pracowników
    przedmioty_pracownikow = [
        (1, 1), (1, 5), (1, 10), (1, 15), (2, 2), (2, 4), (2, 7), (3, 3), (3, 6), (3, 9),
        (4, 8), (4, 14), (4, 19), (5, 11), (5, 12), (5, 17), (6, 13), (6, 18), (7, 16), (7, 20),
        (7, 21), (8, 2), (8, 3), (8, 5), (8, 9), (9, 4), (9, 10), (9, 15), (10, 1), (10, 7),
        (10, 8), (11, 12), (11, 14), (12, 6), (12, 20), (12, 21), (13, 16), (13, 19), (14, 5), (14, 10),
        (14, 13), (15, 2), (15, 4), (15, 18), (16, 3), (16, 7), (17, 8), (17, 11), (17, 12), (18, 13),
        (18, 14), (18, 17), (19, 6), (19, 9), (20, 1), (20, 4), (20, 10)
    ]
    cursor.executemany("INSERT INTO przedmioty_pracownikow (id_pracownika, id_przedmiotu) VALUES (?, ?)", przedmioty_pracownikow)

    # Hospitacje
    protokol = """ [
    {
        "nazwa": "Informacje wstępne",
        "opis": "",
        "info": [
        {
            "pytanie": "Prowadzący zajęcia jednostka organizacyjna:",
            "odpowiedz": "Jan Kowalski"
        },
        {
            "pytanie": "Kod przedmiotu:",
            "odpowiedz": "W041ST-S10018L"
        },
        {
            "pytanie": "Sposób realizacji (tradycyjny, zdalny):",
            "odpowiedz": "tradycyjny"
        }
        ]
    },
    {
        "nazwa": "Ocena formalna zajęć",
        "opis": "",
        "info": [
        {
            "pytanie": "Czy zajęcia zaczęły się punktualnie (tak, nie, ile spóźnienia):",
            "odpowiedz": "5 minut spóźnienia"
        },
        {
            "pytanie": "Czy sprawdzono obecność studentów. Jeżeli tak podać liczbę obecnych:",
            "odpowiedz": "tak, 14 obecnych"
        },
        {
            "pytanie": "Czy sala i jej wyposażenie są przystosowane do formy prowadzonych zajęć. Jeżeli nie to z jakich powodów:",
            "odpowiedz": "tak"
        }
        ]
    },
    {
        "nazwa": "Ocena merytoryczna i metodyczna przeprowadzonych zajęć",
        "opis": "5,5 - wzorowa, 5 - bardzo dobra, 4 - dobra, 3 - dostateczna, 2 - negatywna, 0 - nie dotyczy",
        "info": [
        {
            "pytanie": "Fajność",
            "odpowiedz": "5,5"
        }
        ]
    }
    ]"""

    hospitacje = [
        (30, 'Sala 107b, bud. D-2', '2025-04-15', 1, 1, 1, protokol, '2025-04-29', '2025-05-03'),
        (25, 'Sala 204, bud. B-3', '2025-05-03', 1, 5, 1, protokol, '2025-05-17', None),
        (20, 'Sala 303, bud. E-1', '2025-12-10', 1, 2, 2, protokol, None, None),
        (35, 'Sala 101, bud. C-1', '2025-12-18', 2, 7, 3, protokol, '2026-01-01', '2026-01-15'),
        (28, 'Sala 110, bud. F-4', '2025-02-15', 3, 3, 2, protokol, '2025-03-01', '2025-03-15'),
        (22, 'Sala 305, bud. B-2', '2025-06-03', 4, 4, 1, protokol, '2025-06-17', '2025-07-01'),
        (24, 'Sala 212, bud. D-3', '2025-06-12', 4, 6, 3, protokol, '2025-06-26', '2025-07-10'),
        (32, 'Sala 402, bud. A-1', '2025-04-28', 5, 11, 2, protokol, '2025-05-12', '2025-05-26'),
        (21, 'Sala 308, bud. E-5', '2025-05-20', 6, 9, 3, protokol, '2025-06-03', '2025-06-17'),
        (26, 'Sala 404, bud. C-3', '2025-01-20', 7, 8, 1, protokol, '2025-02-03', '2025-02-17'),
        (30, 'Sala 101, bud. A-4', '2025-06-15', 8, 13, 2, protokol, '2025-06-29', '2025-07-13'),
        (28, 'Sala 207, bud. B-4', '2025-12-05', 9, 10, 1, protokol, '2025-12-19', '2026-01-02'),
        (25, 'Sala 202, bud. D-1', '2025-11-18', 10, 12, 3, protokol, '2025-12-02', '2025-12-16'),
        (22, 'Sala 106, bud. F-5', '2025-05-05', 11, 14, 2, protokol, '2025-05-19', '2025-06-02'),
        (20, 'Sala 308, bud. C-2', '2025-04-22', 12, 15, 1, protokol, '2025-05-06', '2025-05-20'),
        (30, 'Sala 310, bud. A-3', '2025-06-17', 13, 17, 3, protokol, '2025-07-01', '2025-07-15'),
        (35, 'Sala 107b, bud. E-4', '2025-02-25', 14, 16, 2, protokol, '2025-03-11', '2025-03-25'),
        (25, 'Sala 205, bud. B-1', '2025-04-10', 15, 20, 1, protokol, '2025-04-24', '2025-05-08')
    ]

    cursor.executemany('''
        INSERT INTO hospitacje (
            liczba_osob_zapisanych, miejsce, termin, hospitowany_id, przedmiot_id, 
            harmonogram_id, zawartosc_protokolu, data_sporzadzenia, data_zatwierdzenia
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', hospitacje)


    zespoly_hospitujace = [
        (1, 1), (1, 2), (2, 1), (2, 3), (3, 4), (3, 1), (4, 2), (4, 3), (5, 4), (5, 1),
        (6, 2), (6, 4), (7, 5), (7, 6), (8, 1), (8, 3), (9, 4), (9, 5), (10, 6)
    ]
    cursor.executemany("INSERT INTO zespoly_hospitujace (id_hospitacji, id_hospitujacego) VALUES (?, ?)", zespoly_hospitujace)
        
    conn.commit()
    conn.close()