from sqlalchemy.orm import Session
from app.models import Province, City, District, Village
import os
from sqlalchemy import text

# Membuat path absolut
base_dir = os.path.dirname(os.path.abspath(__file__))

def execute_sql_from_file(file_name: str, db_session: Session):
    """
    Membaca dan menjalankan file SQL menggunakan session SQLAlchemy.
    """
    file_path = os.path.join(base_dir, 'sql', file_name)
    
    # Memastikan file ada sebelum mencoba membacanya
    if not os.path.isfile(file_path):
        print(f"File SQL '{file_name}' tidak ditemukan di path: {file_path}")
        return

    try:
        with open(file_path, 'r') as sql_file:
            sql_commands = sql_file.read()

        # Menjalankan SQL menggunakan text()
        db_session.execute(text(sql_commands))
        db_session.commit()  # Commit perubahan jika berhasil
        print(f"SQL dari file '{file_name}' berhasil dijalankan.")
    except Exception as e:
        print(f"Terjadi kesalahan saat mengeksekusi file SQL '{file_name}': {e}")
        db_session.rollback()  # Rollback jika ada error
    finally:
        print(f"Proses eksekusi file SQL '{file_name}' selesai.")

def generate_location_data(session: Session):
    """
    Seeder untuk data lokasi (Province, City, District, Village).
    """
    try:
        execute_sql_from_file("location_provinces.sql", session)
        execute_sql_from_file("location_city.sql", session)
        execute_sql_from_file("location_district.sql", session)
        execute_sql_from_file("location_village.sql", session)
        print("Data lokasi telah berhasil di-seed.")
    except Exception as e:
        print(f"Terjadi kesalahan saat seeding data lokasi: {e}")
        session.rollback()
    finally:
        print("Proses seeding data lokasi selesai.")

def delete_all_locations(session: Session):
    """
    Menghapus semua data lokasi (Village, District, City, Province).
    """
    try:
        session.query(Village).delete()
        session.query(District).delete()
        session.query(City).delete()
        session.query(Province).delete()
        session.commit()  # Commit setelah penghapusan
        print("Data lokasi telah dihapus.")
    except Exception as e:
        print(f"Terjadi kesalahan saat menghapus data lokasi: {e}")
        session.rollback()  # Rollback jika terjadi kesalahan
    finally:
        print("Proses penghapusan data lokasi selesai.")
