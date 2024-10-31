from faker import Faker
from datetime import datetime
from uuid import uuid4
from app.models.auth import Provider
from app.models.user import User
from bson import ObjectId

fake = Faker()

async def seed(db):
    # Fetch sample user IDs to associate with authentications
    users = await db["users"].find().to_list(10)
    user_ids = [user["_id"] for user in users]
    
    # Prepare authentication data
    authentication_data = []
    email_auth_data = []
    google_auth_data = []

    for i, user_id in enumerate(user_ids):
        # Authentication entry
        auth_id = ObjectId()
        provider = Provider.EMAIL if i % 2 == 0 else Provider.GOOGLE
        authentication_data.append({
            "_id": auth_id,
            "authentication_id": str(uuid4()),
            "provider": provider,
            "user": user_id,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        })

        # Specific provider authentication entries
        if provider == Provider.EMAIL:
            email_auth_data.append({
                "email_authentication_id": str(uuid4()),
                "password": fake.password(length=10),
                "user": user_id,
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            })
        else:
            google_auth_data.append({
                "google_authentication_id": str(uuid4()),
                "google_id": f"google_{uuid4()}",
                "user": user_id,
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            })

    # Insert data into collections
    await db["authentications"].insert_many(authentication_data)
    await db["email_authentications"].insert_many(email_auth_data)
    await db["google_authentications"].insert_many(google_auth_data)

    print("Seeded 'authentications', 'email_authentications', and 'google_authentications' collections with sample data.")
