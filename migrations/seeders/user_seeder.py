from faker import Faker
from uuid import uuid4
from sqlalchemy.orm import Session
from app.models import (
    User, EventOrganizer, Provider, Role, UserStatus, Gender,
    OrganizerStatus, ProviderName, Province, City, District, Village, OTP, PersonalAccessToken
)
from app.core.security import generate_password_hash
import random
from sqlalchemy.sql import select

fake = Faker()

def generate_custom_phone_number():
    return '08' + ''.join([str(fake.random_digit()) for _ in range(10)])

def create_user_admin(session: Session):
    user_admin = User(
        full_name="Admin",
        email="admin@example.com",
        password_hash=generate_password_hash("password"),
        role=Role.ADMIN,
        status=UserStatus.PREMIUM,
        gender=Gender.MALE,
        email_verified_at=fake.date_time_this_year(),
        created_at=fake.date_time_this_year(),
        updated_at=fake.date_time_this_year(),
        address=fake.address(),
        phone_number=generate_custom_phone_number(),
        birth_date=fake.date_of_birth(),
        providers=[Provider(provider_name=ProviderName.EMAIL)]
    )
    session.add(user_admin)
    session.commit()
    print("Admin user created.")
    
def create_event_organizer_test(session: Session):
    provinces = session.execute(select(Province)).scalars().all()
    
    selected_province = random.choice(provinces)
    selected_city = random.choice(
        session.execute(select(City).where(City.code_province == selected_province.code_province)).scalars().all()
    )
    selected_district = random.choice(
        session.execute(select(District).where(District.code_city == selected_city.code_city)).scalars().all()
    )
    selected_village = random.choice(
        session.execute(select(Village).where(Village.code_district == selected_district.code_district)).scalars().all()
    )

    user_organizer = User(
        full_name="Organizer",
        email="eo@example.com",
        password_hash=generate_password_hash("password"),
        role=Role.EO,
        status=UserStatus.PREMIUM,
        gender=fake.random_element(list(Gender)),
            email_verified_at=fake.date_time_this_year(),
            address=fake.address(),
            phone_number=generate_custom_phone_number(),
            birth_date=fake.date_of_birth(),
            providers=[Provider(provider_name=ProviderName.EMAIL)]
        )

    organizer = EventOrganizer(
        organizer_id=uuid4(),
        company_name=fake.company(),
        company_address=fake.address(),
        status=OrganizerStatus.ACTIVE,
        verified_at=fake.date_time_this_year(),
        province=selected_province,
        city=selected_city,
        district=selected_district,
        village=selected_village,
        user=user_organizer
    )
    session.add(organizer)
    session.commit()
    print(f"Test event organizer created.")

def create_event_organizer(session: Session, count=5):
    provinces = session.execute(select(Province)).scalars().all()

    for _ in range(count):
        selected_province = random.choice(provinces)
        selected_city = random.choice(
            session.execute(select(City).where(City.code_province == selected_province.code_province)).scalars().all()
        )
        selected_district = random.choice(
            session.execute(select(District).where(District.code_city == selected_city.code_city)).scalars().all()
        )
        selected_village = random.choice(
            session.execute(select(Village).where(Village.code_district == selected_district.code_district)).scalars().all()
        )

        user_organizer = User(
            full_name=fake.name(),
            email=fake.email(),
            password_hash=generate_password_hash("password"),
            role=Role.EO,
            status=UserStatus.PREMIUM,
            gender=fake.random_element(list(Gender)),
            email_verified_at=fake.date_time_this_year(),
            address=fake.address(),
            phone_number=generate_custom_phone_number(),
            birth_date=fake.date_of_birth(),
            providers=[Provider(provider_name=ProviderName.EMAIL)]
        )

        organizer = EventOrganizer(
            organizer_id=uuid4(),
            company_name=fake.company(),
            company_address=fake.address(),
            status=OrganizerStatus.ACTIVE,
            verified_at=fake.date_time_this_year(),
            province=selected_province,
            city=selected_city,
            district=selected_district,
            village=selected_village,
            user=user_organizer
        )
        session.add(organizer)
    session.commit()
    print(f"{count} event organizers created.")

def create_user_test(session: Session):
    user_test = User(
        full_name="Test",
        email="test@example.com",
        password_hash=generate_password_hash("password"),
        role=Role.USER,
        status=UserStatus.BASIC,
        email_verified_at=fake.date_time_this_year(),
        created_at=fake.date_time_this_year(),
        updated_at=fake.date_time_this_year(),
        address=fake.address(),
        phone_number=generate_custom_phone_number(),
        birth_date=fake.date_of_birth(),
        providers=[Provider(
            provider_name=ProviderName.EMAIL,
        )],   
    )
    
    session.add(user_test)
    session.commit()
    print("Test user created.")
    
def create_users(session: Session, count=10):
    for _ in range(count):
        user = User(
            full_name=fake.name(),
            email=fake.email(),
            password_hash=generate_password_hash("password"),
            role=Role.USER,
            status=UserStatus.BASIC,
            email_verified_at=fake.date_time_this_year(),
            created_at=fake.date_time_this_year(),
            updated_at=fake.date_time_this_year(),
            address=fake.address(),
            phone_number=generate_custom_phone_number(),
            birth_date=fake.date_of_birth(),
            providers=[Provider(
                provider_name=ProviderName.EMAIL,
            )],
        )
        session.add(user)
    session.commit()
    print(f"Generated {count} users.")
    
def delete_all_users(session: Session):
    session.query(PersonalAccessToken).delete()
    session.query(OTP).delete()
    session.query(Provider).delete()
    session.query(EventOrganizer).delete()
    session.query(User).delete()
    session.commit()
    print("All users deleted.")