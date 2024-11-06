from faker import Faker
from datetime import datetime
from app.models.user import Gender, Role, UserStatus, User
from bson import ObjectId
import re
from beanie import init_beanie

fake = Faker()

async def seed(db):
    # Initialize Beanie
    await init_beanie(database=db, document_models=[User])
    
    data = []

    for i in range(10):  # Combine the loops since both are generating the same type of data
        NIK = f"{fake.unique.random_int(min=1000000000000000, max=9999999999999999)}"  # 16 digit NIK as string
        phone_number = re.sub(r'\D', '', fake.phone_number())  # Remove non-digits
        
        # Ensure the phone number starts with '08' and is <= 16 digits
        if len(phone_number) + 2 <= 16:  # 2 for '08'
            phone_number = '08' + phone_number
        else:
            phone_number = '08' + phone_number[:14]  # Limit phone number to 16 digits
        
        # Create the user object
        user = User(
            user_id=ObjectId(),
            full_name=fake.name(),  # Corrected here
            email=f"test{i}@example.com" if i < 3 else fake.unique.email(),  # Use sequential emails for first 3, then unique
            gender=Gender.MALE if fake.boolean() else Gender.FEMALE,
            birth_date=fake.date_of_birth(minimum_age=18, maximum_age=60),
            phone_number=phone_number,
            NIK=NIK,
            address=fake.address(),
            role=Role.USER,
            status=UserStatus.BASIC,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        # Add the user to the data list
        data.append(user)
    
    # Insert the generated data into MongoDB
    await db["users"].insert_many([user.dict() for user in data])  # Use .dict() to serialize data for insertion
    
    print("Seeded 'users' collection with sample data.")

