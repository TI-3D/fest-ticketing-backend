from faker import Faker
from datetime import datetime
from app.models.user import Gender, Role, UserStatus, User
from bson import ObjectId
import re
from beanie import init_beanie

fake = Faker()

async def seed(db):
    await init_beanie(database=db, document_models=[User])
    data = []
    for i in range(3):
        NIK = str(fake.unique.random_int(min=1000000000000000, max=9999999999999999)).zfill(16)  # Ensure it's 16 digits
        phone_number = re.sub(r'\D', '', fake.phone_number())
        
        # Prepend "08" and ensure the total length is <= 16
        if len(phone_number) + 2 <= 16:  # 2 for '08'
            phone_number = '08' + phone_number
        else:
            phone_number = '08' + phone_number[:14] 
        data.append(
            User(
                user_id=ObjectId(),
                full_name=fake.name(),
                email=(f"test{i}@example.com"),
                gender=Gender.MALE if fake.boolean() else Gender.FEMALE,
                birth_date=fake.date_of_birth(minimum_age=18, maximum_age=60),
                phone_number=phone_number,
                NIK=NIK,
                address=fake.address(),
                role=Role.USER,
                status=UserStatus.BASIC,
                email_verified_at=datetime.now(),
                created_at=datetime.now(),
                updated_at=datetime.now()
            ).model_dump()
        )
    
    for _ in range(7):
        NIK = str(fake.unique.random_int(min=1000000000000000, max=9999999999999999)).zfill(16)  # Ensure it's 16 digits
        phone_number = re.sub(r'\D', '', fake.phone_number())
        
        # Prepend "08" and ensure the total length is <= 16
        if len(phone_number) + 2 <= 16:  # 2 for '08'
            phone_number = '08' + phone_number
        else:
            phone_number = '08' + phone_number[:14] 
        data.append(User(
            user_id=ObjectId(),
            full_name=fake.name(),
            email=fake.unique.email(),
            gender=Gender.MALE if fake.boolean() else Gender.FEMALE,
            birth_date=fake.date_of_birth(minimum_age=18, maximum_age=60),
            phone_number=phone_number,
            NIK=NIK,
            address=fake.address(),
            role=Role.USER,
            status=UserStatus.BASIC,
            email_verified_at=datetime.now(),
            created_at=datetime.now(),
            updated_at=datetime.now()
        ).model_dump())

    await db["users"].insert_many(data)
    print("Seeded 'users' collection with sample data.")
