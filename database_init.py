import os
from repo.db import create_tables, insert_initial_data

def main():
    if os.path.exists('database.db'):
        print('Usuwanie istniejącej bazy danych')
        os.remove('database.db')
    
    create_tables()
    
    insert_initial_data()
    
    print("Baza danych została stworzona i dane zostały dodane.")

if __name__ == "__main__":
    main()