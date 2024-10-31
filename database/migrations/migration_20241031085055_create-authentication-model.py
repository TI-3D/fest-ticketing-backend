
from pymongo import ASCENDING, IndexModel
from pymongo.errors import CollectionInvalid
from app.models.auth import Authentication, EmailAuthentication, GoogleAuthentication  # Adjust according to your structure
from database.utils import generate_validation_schema

def upgrade(db):
    # Authentication collection
    try:
        auth_schema = generate_validation_schema(Authentication)
        db.create_collection("authentications", validator=auth_schema)
        db["authentications"].create_indexes([
            IndexModel([("authentication_id", ASCENDING)], unique=True),
            IndexModel([("provider", ASCENDING)])
        ])
        print("Collection 'authentications' created with validation and indexes.")
    except CollectionInvalid:
        print("Collection 'authentications' already exists. Skipping creation.")

    # EmailAuthentication collection
    try:
        email_auth_schema = generate_validation_schema(EmailAuthentication)
        db.create_collection("email_authentications", validator=email_auth_schema)
        db["email_authentications"].create_indexes([
            IndexModel([("email_authentication_id", ASCENDING)], unique=True),
            IndexModel([("user", ASCENDING)])
        ])
        print("Collection 'email_authentications' created with validation and indexes.")
    except CollectionInvalid:
        print("Collection 'email_authentications' already exists. Skipping creation.")

    # GoogleAuthentication collection
    try:
        google_auth_schema = generate_validation_schema(GoogleAuthentication)
        db.create_collection("google_authentications", validator=google_auth_schema)
        db["google_authentications"].create_indexes([
            IndexModel([("google_authentication_id", ASCENDING)], unique=True),
            IndexModel([("user", ASCENDING)])
        ])
        print("Collection 'google_authentications' created with validation and indexes.")
    except CollectionInvalid:
        print("Collection 'google_authentications' already exists. Skipping creation.")

def downgrade(db):
    db.drop_collection("authentications")
    db.drop_collection("email_authentications")
    db.drop_collection("google_authentications")
    print("Collections 'authentications', 'email_authentications', and 'google_authentications' dropped.")
