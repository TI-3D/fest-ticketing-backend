from faker import Faker
from datetime import datetime
from app.models.user import Gender, Role, UserStatus
from uuid import uuid4

fake = Faker()

async def seed(db):
    data = []
    for i in range(3):
        birth_date = fake.date_of_birth(minimum_age=18, maximum_age=60)
        data.append({
            "user_id": str(uuid4()),
            "full_name": fake.name(),
            # "email": fake.unique.email(),
            'email': f"test{i}@example.com",
            "gender": Gender.MALE if fake.boolean() else Gender.FEMALE,
            "birth_date": datetime.combine(birth_date, datetime.min.time()), 
            "phone_number": fake.phone_number(),
            "NIK": str(fake.unique.random_number(digits=16)),
            "address": fake.address(),
            "role": Role.USER,
            "status": UserStatus.BASIC,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        })
    
    for _ in range(7):
        birth_date = fake.date_of_birth(minimum_age=18, maximum_age=60)
        data.append({
            "user_id": str(uuid4()),
            "full_name": fake.name(),
            "email": fake.unique.email(),
            "gender": Gender.MALE if fake.boolean() else Gender.FEMALE,
            "birth_date": datetime.combine(birth_date, datetime.min.time()), 
            "phone_number": fake.phone_number(),
            "NIK": str(fake.unique.random_number(digits=16)),
            "address": fake.address(),
            "role": Role.USER,
            "status": UserStatus.BASIC,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        })

    await db["users"].insert_many(data)
    print("Seeded 'users' collection with sample data.")
