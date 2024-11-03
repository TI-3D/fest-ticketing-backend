from app.models.personal_access_token import PersonalAccessToken
from database.utils import generate_validation_schema
from pymongo import ASCENDING, IndexModel
from pymongo.errors import CollectionInvalid


def upgrade(db):
    try: 
        personal_access_token_schema = generate_validation_schema(PersonalAccessToken)
        db.create_collection("personal_access_tokens", validator=personal_access_token_schema)
        db["personal_access_tokens"].create_indexes([
            IndexModel([("personal_access_token_id", ASCENDING)], unique=True),
            IndexModel([("user_id", ASCENDING)])
        ])
        
        print("Collection 'personal_access_tokens' created with validation and indexes.")
    except CollectionInvalid:
        print("Collection 'personal_access_tokens' already exists. Skipping creation.")


def downgrade(db):    
    db.drop_collection("personal_access_tokens")
    print("Collection 'personal_access_tokens' dropped.")
