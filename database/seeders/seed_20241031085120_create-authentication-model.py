from faker import Faker
from datetime import datetime
from uuid import uuid4
from app.models.auth import Provider, Authentication, EmailAuthentication, GoogleAuthentication
from bson import ObjectId
from app.core.security import hash_password
from beanie import init_beanie

fake = Faker()

async def seed(db):
    await init_beanie(database=db, document_models=[Authentication, EmailAuthentication, GoogleAuthentication])
    # Fetch sample user IDs to associate with authentications
    users = await db["users"].find().to_list(10)
    user_ids = [user["user_id"] for user in users]
    
    # Prepare authentication data
    authentication_data = []
    email_auth_data = []
    google_auth_data = []

    for i, user_id in enumerate(user_ids):
        # Authentication entry
        auth_id = ObjectId()
        provider = Provider.EMAIL
        authentication_data.append(
            Authentication(
                authentication_id=auth_id,
                provider=provider,
                user_id=user_id,
                created_at=datetime.now(),
                updated_at=datetime.now()
            ).model_dump()
        )

        # Specific provider authentication entries
        if provider == Provider.EMAIL:
            email_auth_data.append(
                EmailAuthentication(
                    email_authentication_id=ObjectId(),
                    password=hash_password('password123'),
                    user_id=user_id,
                    email_verified_at=datetime.now(),
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                ).model_dump()
            )
        else:
            google_auth_data.append(
                GoogleAuthentication(
                    google_authentication_id=ObjectId(),
                    google_id=f"google_{uuid4()}",
                    user_id=user_id,
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                ).model_dump()
            )

    # Insert data into collections
    if authentication_data:
        await db["authentications"].insert_many(authentication_data)
    if email_auth_data:
        await db["email_authentications"].insert_many(email_auth_data)
    if google_auth_data:
        await db["google_authentications"].insert_many(google_auth_data)

    print("Seeded 'authentications', 'email_authentications', and 'google_authentications' collections with sample data.")
