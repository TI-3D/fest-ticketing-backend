from app.core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from migrations.seeders.user_seeder import create_user_admin, create_user_test, create_users, create_event_organizer, create_event_organizer_test, delete_all_users
from migrations.seeders.event_category_seeder import create_event_categories, delete_all_event_categories
from migrations.seeders.location_seeder import generate_location_data, delete_all_locations
from migrations.seeders.event_seeder import create_events, delete_all_events
# Initialize the database engine with settings from config
engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True, echo=True)

# Create a session local for interacting with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def seed_db():
    """
    Seeds the database with an admin user, a test user, and a few random users.
    """
    db = SessionLocal()  # Open a new database session
    try:
        delete_all()  # Delete all data from the database before seeding
        
        # Location seeder
        generate_location_data(db)
        
        # User seeders
        create_user_admin(db)
        create_user_test(db)
        create_users(db, 5)  # Create 5 random users
        create_event_organizer_test(db)
        create_event_organizer(db, 5)  # Create 5 random event organizers
        
        # Event category seeder
        create_event_categories(db)
        
        # Event seeder
        create_events(db, 10)  # Create 10 random events
    finally:
        db.close()  # Close the session after seeding
        print("Seeding complete.")  # Indicate completion of the seeding process

def delete_all():
    """
    Deletes all data from the database.
    """
    db = SessionLocal()  # Open a new database session
    try:
        delete_all_events(db)
        delete_all_users(db)
        delete_all_locations(db)
        delete_all_event_categories(db)
    finally:
        db.close()  # Close the session after deletion
        print("Deletion complete.")  # Indicate completion of the deletion process
if __name__ == "__main__":
    # Execute the seeding process when the script is run directly
    seed_db()
