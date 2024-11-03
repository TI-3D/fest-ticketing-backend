from pymongo import ASCENDING, IndexModel
from pymongo.errors import CollectionInvalid
from app.models import User  # Adjust import according to your project structure
from database.utils import generate_validation_schema

def upgrade(db):
    # Generate validation schema from the User model
    validation_schema = generate_validation_schema(User)

    # Define the collection schema (indexes and validation)
    try:
        db.create_collection("users", validator=validation_schema)

        # Create indexes for the collection
        db["users"].create_indexes([
            IndexModel([("email", ASCENDING)], unique=True),
            IndexModel([("user_id", ASCENDING)], unique=True)
        ])

        print("Collection 'users' created with validation and indexes on 'email' and 'user_id'.")

    except CollectionInvalid:
        print("Collection 'users' already exists. Skipping creation.")

def downgrade(db):
    db.drop_collection("users")
    print("Collection 'users' dropped.")
