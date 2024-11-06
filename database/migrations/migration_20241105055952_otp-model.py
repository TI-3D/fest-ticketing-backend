from pymongo import ASCENDING, IndexModel
from pymongo.errors import CollectionInvalid
from app.models import OTP  # Adjust import according to your project structure
from database.utils import generate_validation_schema

def upgrade(db):
    validation_schema = generate_validation_schema(OTP)
    try:
        db.create_collection(
            "otps",
            validator=validation_schema,
        )
        db["otps"].create_indexes(
            [
                IndexModel([("otp_id", ASCENDING)], unique=True),
                IndexModel([("email", ASCENDING)], unique=True),
            ]
        )
        
        print("Collection 'otps' created successfully")
    except CollectionInvalid:
        print("Collection 'otps' already exists")

def downgrade(db):
    db.drop_collection("otps")
    print("Collection 'otps' dropped")
