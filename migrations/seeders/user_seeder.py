from faker import Faker
from uuid import uuid4
from sqlalchemy.orm import Session
from app.models import (
    User, EventOrganizer, Provider, Role, UserStatus, Gender,
    OrganizerStatus, ProviderName, Province, City, District, Village
)
from app.core.security import generate_password_hash

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
    


def create_event_organizer(session: Session, count=5):
    provinces = session.query(Province).all()
    cities = session.query(City).all()
    districts = session.query(District).all()
    villages = session.query(Village).all()

    for _ in range(count):
        province = fake.random_element(provinces)
        city = fake.random_element(cities)
        district = fake.random_element(districts)
        village = fake.random_element(villages)

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
            province=province,
            city=city,
            district=district,
            village=village,
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
    session.query(Provider).delete()
    session.query(EventOrganizer).delete()
    session.query(User).delete()
    session.commit()
    print("All users deleted.")