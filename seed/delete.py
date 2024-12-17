from app.core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from seed.seeders.user_seeder import delete_all_users
from seed.seeders.event_category_seeder import delete_all_event_categories
from seed.seeders.event_seeder import delete_all_events
from seed.seeders.payment_seeder import delete_all_payments
# Initialize the database engine with settings from config
engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True, echo=True)

# Create a session local for interacting with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def delete_all():
    """
    Deletes all data from the database.
    """
    db = SessionLocal()  # Open a new database session
    try:
        delete_all_payments(db)
        delete_all_events(db)
        delete_all_users(db)
        delete_all_event_categories(db)
    finally:
        db.close()  # Close the session after deletion
        print("Deletion complete.")  # Indicate completion of the deletion process
        
if __name__ == "__main__":
    # Execute the seeding process when the script is run directly
    delete_all()
